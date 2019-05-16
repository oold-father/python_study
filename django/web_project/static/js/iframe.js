function setIframeHeight(iframe) {
if (iframe) {
var iframeWin = iframe.contentWindow || iframe.contentDocument.parentWindow;
if (iframeWin.document.body) {
iframe.height = iframeWin.document.documentElement.scrollHeight || iframeWin.document.body.scrollHeight;
}
}
}
window.onload = function () {
setIframeHeight(document.getElementById('test_iframe'));
}

// function finish() {
//     var bott = document.getElementById('finish');
//     bott.style.display = "block";
//
// }

