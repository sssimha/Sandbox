// New - works
javascript:w=window;l=w.location;try{v=window.open("chm:"+document.location);v.close();}catch(err){}try{if(w.location!=l){w.history.back();}}catch(err){}

//Old
javascript:w=window;l=w.location;v=window.open("chm:"+document.location);v.close();if(w.location!=l){w.history.back();}
