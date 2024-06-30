from .models import Folder
from .utils import SVGS
from django.db.models import QuerySet
import asyncio 

def renderFiles(request):
    result = ''
    if not request.user.is_authenticated: 
        return result
    rootFolder, created = Folder.objects.get_or_create(name=f'{request.user.username}-root-folder', user=request.user)
    files: QuerySet = rootFolder.files.all() 
    folders: QuerySet = rootFolder.sub_folders.all()
    everything = list(files) + list(folders)
    # asyncio.run(asyncio.sleep(2)) # intentional delay
    for item in everything: 
        result += f"""
            <li class="mb-3 rounded file" x-data="{{'open':false}}">
                <div class="dots rounded" @click="open=!open">
                    <svg role="button" class="dropdown-toggle" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" style="fill: steelblue;"><path d="M12 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg>               
                    <div  x-show="open" class="dropdown-content rounded" @click.outside="open=false">
                        <ul>
                            <li><span><svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" class="fill-gray-400"><path d="M5 20a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8h2V6h-4V4a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2v2H3v2h2zM9 4h6v2H9zM8 8h9v12H7V8z"></path><path d="M9 10h2v8H9zm4 0h2v8h-2z"></path></svg></span> <span>Delete</span></li>
                            <li><span><svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" class="fill-gray-400"><path d="M3 12c0 1.654 1.346 3 3 3 .794 0 1.512-.315 2.049-.82l5.991 3.424c-.018.13-.04.26-.04.396 0 1.654 1.346 3 3 3s3-1.346 3-3-1.346-3-3-3c-.794 0-1.512.315-2.049.82L8.96 12.397c.018-.131.04-.261.04-.397s-.022-.266-.04-.397l5.991-3.423c.537.505 1.255.82 2.049.82 1.654 0 3-1.346 3-3s-1.346-3-3-3-3 1.346-3 3c0 .136.022.266.04.397L8.049 9.82A2.982 2.982 0 0 0 6 9c-1.654 0-3 1.346-3 3z"></path></svg></span> <span>Share</span></li>
                        </ul>
                    </div>
                </div>
                
                <div class="flex justify-center">
                    {SVGS.get('folder') if item.isFolder() else SVGS.get(item.extension) or SVGS.get('generic')}
                </div>

                
                <a href="#" class="filename block text-center mt-1 truncate">
                    {item.name}
                </a>
            </li>
        """
    return result
        
    