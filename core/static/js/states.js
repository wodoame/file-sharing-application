document.addEventListener('alpine:init', ()=>{
    Alpine.data('navImage', ()=>({
        url:undefined,
        loaded: false,
        init(){
          this.getImage();
        }, 

        async getImage(){
            const response = await fetch('https://avatars.githubusercontent.com/u/98283377?v=4');
            const blob = await response.blob();
            this.url = URL.createObjectURL(blob);
            this.loaded = true;
          }
      }));
});