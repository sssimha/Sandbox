// New - works
javascript:w=window;pattern=/([\^&\|\\<>]+)\x?/g;l=w.location;l_s=String(l).replace(pattern,'^^^$1');window.alert(l_s);try{v=window.open("chm:"+l_s);v.close();}catch(err){}try{if(w.location!=l){w.history.back();}}catch(err){}

//Old
javascript:w=window;l=w.location;v=window.open("chm:"+document.location);v.close();if(w.location!=l){w.history.back();}
