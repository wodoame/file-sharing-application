from .models import Folder
from .utils import SVGS
import asyncio 

def renderFiles(request):
    result = ''
    if not request.user.is_authenticated: 
        return result
    rootFolder, created = Folder.objects.get_or_create(name=f'{request.user.username}-root-folder', user=request.user)
    files = rootFolder.files.all() 
    asyncio.run(asyncio.sleep(2)) # intentional delay
    for file in files: 
        result += f"""
            <li class="mb-3 rounded file" x-data="{{'open':false}}">
                <div class="dots rounded" @click="open=!open">
                    <svg role="button" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" style="fill: steelblue;"><path d="M12 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg>               
                    <div  x-show="open" class="dropdown-content rounded" @click.outside="open=false">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatibus
                    </div>
                </div>
                
                <div class="flex justify-center">
                    {SVGS.get(file.extension) or SVGS.get('generic')}
                </div>

                <div class="filename text-center mt-1 truncate">
                    {file.name}
                </div>
            </li>
        """
    return result
        
    