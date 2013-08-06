setup_filecollector = function($, uploadedWidgetHtmlName, sendbutton_selector, doSubmitLock){
    /*

      $ - jQuery prefix
      uploadedWidgetHtmlName - django input widget name, for request parsing
      sendbutton_selector - submit, which will send request, it will be locked while uploading if doSubmitLock is set to true
      doSubmitLock - variable which controlls locking while uploading

    */

    $(document).ready(function(){
	    function collectfiles(){
		    var files_inputs = '';
		    $('.filelink').each(function(i, el) { 
			    files_inputs += '<input type="hidden" value="'+$(el).attr('id')+'" name="'+uploadedWidgetHtmlName+'"/>';
		    });
		    $("#hidden_container").append(files_inputs);
	    };

        $(sendbutton_selector).click(function(e){
		    if (doSubmitLock){
          	        var isUploading = $(".fileupload-progressbar").is(":visible");

			        if (isUploading){
				        e.preventDefault();
			        }
			        else {
				        collectfiles();
			        }
			   }
		    else
			    collectfiles();
	    });
    });
}