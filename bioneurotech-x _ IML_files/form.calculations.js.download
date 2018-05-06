
var oneminute=60;
var lastactionobj="";

var user_agent = navigator.userAgent;
var is_android = window.is_android;
var ie_version=window.ie_version;
var may_scroll=window.may_scroll;
var calculations_timeout=null;
var fields_timeout=null;


function obj_size(data) {
var length = 0;
for(var prop in data){
    if(data.hasOwnProperty(prop))
        length++;
}	
return length;
}


function myformsavetimer()
{
	
window.fields_timeout=setTimeout('myformsavetimer()', 200);

if (window.lastactiontime>0)
	{
	var timeacum=Math.round(new Date().getTime() );
	var seconds=Math.round((timeacum-window.lastactiontime));
	
	if (seconds<500){
		// Should already have the good status
		}
	else {
		window.lastactiontime=0;
		clearTimeout(window.calculations_timeout);
		updateformfields_async(false,0);
		//clearTimeout(window.calculations_timeout);
		clearTimeout(window.fields_timeout);
		
		}

	}
}

function updateformfields_async(only_summary,level) {
calculations_timeout= setTimeout( function() {updateformfields(only_summary,level); },50);
}

function updateformfields(only_summary,level) {

    try {
        if (window.location.href.indexOf('newPDF=1') !== -1) {
            return;
        }
    } catch (e) {
        // do nothing yet
    }


lastobj_id=0;
if (lastactionobj!=null)
if (typeof(lastactionobj)=="object")
	{ lastobj=lastactionobj;
		if (typeof(lastobj.id)!="undefined") {
			lastobj_id=lastobj.id;
			}
	}

if (!calc_fields) return false;

if (stopCalculateNow()) { window.stopCalculate=false; return false;  }

var controls=$.param($('#mainform123 input[type="text"], #mainform123 input[type="checkbox"]:checked, #mainform123 input[type="radio"]:checked, #mainform123 input[type="hidden"], #mainform123 select').not('.excluded-ajax').not(':hidden'));

if (stopCalculateNow()) { window.stopCalculate=false; return false;  }

if ($('input[name="language"]').length>0) {
	lang=$('input[name="language"]').val();
	controls+="&usedlang="+lang; 
	}

var hidden_page_divs=$('.fieldcontainer.currentPageInactive, .fieldcontainer.class123-hidden, .fieldcontainer.currentPageActive');
var hidden_page_divs_count=hidden_page_divs.length;
var controls_extra="";
var params="";
if (hidden_page_divs_count>0) {
	for (var i=0;i < hidden_page_divs_count;i++) {
		if (stopCalculateNow()) { window.stopCalculate=false; return false;  }
		var hidden_div = hidden_page_divs.eq(i);
		var element_style=hidden_div.attr("style");
		if (element_style==undefined) element_style="";
		if (!hidden_div.hasClass('currentPageActive')) {
		if (((element_style.indexOf("display: none")==-1)) || (hidden_div.hasClass('class123-hidden') )) {  // cu class123-hidden sunt cele ascunse normal
				inputs=hidden_div.find('input[type="text"], input[type="checkbox"]:checked, input[type="radio"]:checked, select').not('.excluded-ajax');
				params=$.param(inputs);
				controls_extra+="&"+params;
		}
		} else {
			if ((hidden_div.hasClass('class123-hidden') ) ||(hidden_div.hasClass('class123-readonly-field') )) {  // cu class123-hidden sunt cele ascunse normal
				inputs=hidden_div.find('input[type="text"],input[type="checkbox"]:checked, input[type="radio"]:checked');
				params=$.param(inputs);
				controls_extra+="&"+params;
				}
			if ((element_style.indexOf("display: none")==-1)&& (hidden_div.find('.searchable').length>0)) {
				inputs=hidden_div.find('select.searchable').not('.excluded-ajax');
				params=$.param(inputs);
				controls_extra+="&"+params;
				}	
		}
                if(hidden_div.hasClass('force-calc')) { // Alen: If TIME field is 24-hour format, calculate hidden fields only => 04.06.2015
                    inputs=hidden_div.find('input[type="text"]:hidden');
		    params=$.param(inputs);
		    controls_extra+="&"+params;
                }
                
	}
}

if($(".stars-rate").length>0){
    inputs = $(".stars-rate").parent().find('input[type="hidden"]');
    params=$.param(inputs);
    controls_extra+="&"+params;
}

if ($('#id123-couponcode').length>0) if (controls_extra.indexOf('couponcode')==-1) { controls_extra+="&couponcode="+$('#id123-couponcode').val(); }

if (this.form_is_quiz) controls_extra+='&form_is_quiz=1';

var hiddenfields="";
if ($('#hiddenfields').length>0) hiddenfields=$('#hiddenfields').val();
var instance="";
if (stopCalculateNow()) { window.stopCalculate=false; return false;  }
if ($('#instance').length>0) instance=$('#instance').val();

$.ajax({
url:"/ajax_form.php?modulename=sf_calc_actions.php",
data:"someaction=get_result&f_id="+fid+"&only_summary="+only_summary+"&curr="+curr+"&"+controls+controls_extra+"&hiddenfields="+hiddenfields+"&instance="+instance,
type:"POST",
async:true,
dataType:"text",
cache:false,
success:function(dat) {
	

	if (stopCalculateNow()) { window.stopCalculate=false; return false;  }
	var data = $.parseJSON(dat);
	var op_count=obj_size(data);
	
		if (op_count>0) {
			var form_invoice="";
			var form_total_val=0;
			var form_subtotal_val=0;
			if ($('#id123-total-pay').length>0) $('#id123-total-pay').val(data.total_val);
			if ($('#id123-control000001').length>0) $('#id123-control000001').val(data.quiz_total);
			if (data.form!=undefined) {var update_count =obj_size(data.form);}
				else update_count=0;
			if ((document.getElementById('realtime-summary')!=undefined)  || (document.getElementById('offline-form-summary')!=undefined)) if (data.summary!=undefined) {  form_invoice+=data.summary; form_total=data.total; form_total_val=data.total_val; form_subtotal_val=data.subtotal_val; }				
				if (update_count>0) {				
				var form_data=data.form;
				for(key in form_data) {
				if (stopCalculateNow()) { window.stopCalculate=false; return false;  }	
				val=form_data[key].toString();
				if (document.getElementById('id123-control'+key)!=undefined) 
					if (document.getElementById('id123-control'+key).id!=lastobj_id) {
						var elem=document.getElementById('id123-control'+key);
						var big_parent=elem.parentNode.parentNode.parentNode;
						var small_parent=elem.parentNode;
						var errors_p=getElementsByClassName(small_parent,'p','fielderror');
						if (val.indexOf('error')==-1) {
							elem.value=val;
							if (errors_p.length==0) {
							big_parent.style.background='';}
							} 
							else { elem.value="";big_parent.style.background='#FFDFDF';
							vals=val.split("||");
							var error_p='<div class="clear"></div><p class="fielderror calculation-error" style="padding: 0px; margin: 0px; color: red; font-weight: bold; ">'+vals[1]+'</p>';}
							var errors_p=getElementsByClassName(small_parent,'p','fielderror');
							if (errors_p.length>0) {
								for (i=0;i<errors_p.length;i++) {
								if (stopCalculateNow()) { window.stopCalculate=false; return false;  }
									if ( $(errors_p[i]).hasClass('calculation-error') ) small_parent.removeChild(errors_p[i]);	
								}
							}
							if (val.indexOf('error')!=-1) { small_parent.innerHTML+=error_p;}
						}
				}
			} else {
			$('input.with-formula').val('');	
			}
		
		var rules_delay=0;
		
		if ($('#id123-self-fid').length>0)
			if (($('#id123-self-fid').val()==1432849) || ($('#id123-self-fid').val()==1470770) || ($('#id123-self-fid').val()==1473556)) // custom delay for big forms
			rules_delay=1000;
		
		if (op_count<60)  
			InputRules2('calculation',0,rules_delay); //  daca sunt prea multe reguli nu se mai aplica ca sa nu fie delay prea mare
		
		$("#id123-button-send").attr("disabled", false);
		if (level<32) if ($('#hiddenfields').val()!=hiddenfields) {  /* updateformfields_async(only_summary,level+1);  */ } // extra refresh
			else
		if (only_summary)  {  
		$('#offline-form-summary').html(form_invoice);
		$('#offline-form-summary').show();//MNG:ca sa se afiseze cand se da click pe calculate
		$('html').animate({scrollTop: $("#offline-form-summary").offset().top-30},400);
		if (form_invoice.length>0)	{if (!$('#offline-form-summary').hasClass('visible')) $('#offline-form-summary').addClass("visible");}
			else { 
				if ($('#offline-form-summary').hasClass('visible')) $('#offline-form-summary').removeClass("visible");
				}
			} else { 
				if (form_subtotal_val!=0) {
				if (document.getElementById('realtime-summary')!=undefined) document.getElementById('realtime-summary').innerHTML=""+form_invoice+"";
				if (document.getElementById('form-total')!=undefined) document.getElementById('form-total').innerHTML=""+form_total+"";
				if ($('#form-summary').hasClass("hidden")) $('#form-summary').removeClass("hidden");	
			} else {
				if (!$('#form-summary').hasClass("hidden")) $('#form-summary').addClass("hidden");	
			}	
	if (is_android==true) if ($('#realtime-summary').length>0)	{
	 $('#realtime-summary').find('#summary-body').css({ overflow:'visible' });	
	} else {						
	if (may_scroll) $('#realtime-summary').find('#summary-body').css({maxHeight:summary_max_height});	
	}		
	if ($('#realtime-summary').find('#summary-body').hasScrollBar()) {
		var inner_table=$('#summary-body-table');
		inner_table.css("width",(inner_table.width()+18)+"px");
		$('#form-total').css("text-indent",-16);
		$('#realtime-summary').find('#summary-body').width($('#form-summary').width());
		}
	}			
	if ((may_scroll) && (real_time)) {
	init_real_time_toolbar();	
	scroll_real_time_toolbar();	
	}
 } //else calculations_timeout=setTimeout(function() { InputRules('calculation'); },0);
if (level<32) if ($('#hiddenfields').val()!=hiddenfields) { updateformfields(only_summary,level+1);  } // extra refresh

//[Raul] below is for a custom client - to update prices again after rules.
if (typeof(fid)!="undefined") if (fid=='1556438') if (level==0)  updateformfields(only_summary,level+1);

	 if (only_summary) RefreshFrameHeight(0);
}
});

}

(function($) {
    $.fn.hasScrollBar = function() {
		if (this.get(0)!=undefined)
        return (this.get(0).scrollHeight-1) > this.height();
    }
})(jQuery);
function getElementsByClassName(oElm, strTagName, strClassName){
    var arrElements = (strTagName == "*" && oElm.all)? oElm.all :
        oElm.getElementsByTagName(strTagName);
    var arrReturnElements = new Array();
    strClassName = strClassName.replace(/\-/g, "\\-");
    var oRegExp = new RegExp("(^|\\s)" + strClassName + "(\\s|$)");
    var oElement;
    for(var i=0; i<arrElements.length; i++){
        oElement = arrElements[i];     
        if(oRegExp.test(oElement.className)){
            arrReturnElements.push(oElement);
        }   
    }
    return (arrReturnElements)
}

myformsavetimer();