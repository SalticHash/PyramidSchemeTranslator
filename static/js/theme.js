
function detectColorScheme(){
    let theme ="light";    //default to light

    //local storage is used to override OS theme settings
    if(localStorage.getItem("theme")){
        if(localStorage.getItem("theme") == "dark"){
            theme = "dark";
        }
    } else if(!window.matchMedia) {
        //matchMedia method not supported
        return false;
    } else if(window.matchMedia("(prefers-color-scheme: dark)").matches) {
        //OS theme setting detected as dark
        theme = "dark";
    }

    document.documentElement.setAttribute("data-theme", theme);

}
function toggleTheme() {
    let theme = document.documentElement.getAttribute("data-theme");
    if (theme == "dark") theme = "light";
    else theme = "dark";
    
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme)

}
detectColorScheme();
