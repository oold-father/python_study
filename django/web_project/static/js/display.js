function open_down(obj) {
    var box = obj.parentNode.id;
    var boxs = document.getElementById(box).getElementsByClassName("n-list")
    if (boxs.length != 0) {
        for (var i = 0; i < boxs.length; i++) {
            if (boxs[i].style.display =="none") {
                boxs[i].style.display = "block";
                    // {#obj.style["background"]="url(../img/4.png) no-repeat"#}
            }
            else if(boxs[i].style.display == "block"){
                boxs[i].style.display = "none"
                     // {#obj.style["background"]="url(../img/3.png) no-repeat"#}
            }
            else {
                alert("出错！")
            }
        }
    }


}

