/* task.js
 * 
 * This file holds the main experiment code.
 * 
 * Requires:
 *   config.js
 *   psiturk.js
 *   utils.js
 */

// Create and initialize the experiment configuration object
var $c = new Config(condition, counterbalance);

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc);

// Preload the HTML template pages that we need for the experiment
psiTurk.preloadPages($c.pages);

// Objects to keep track of the current phase and state
var CURRENTVIEW;
var STATE;

/*************************™
 * INSTRUCTIONS         
 *************************/


 var Instructions = function() {

    $(".slide").hide();

    function slideshow(x){

        var slide = $("#instructions-training-" + x);

        $("#goback").hide();

        if (x == 1){
            $(".tutorial").attr("src",'/static/images/instructions/tutorial1.png');

            slide.fadeIn($c.fade);

            slide.find('#goback').click(function () {
                // this.i--;
                i = inc_i(-1);
                if (i == 1) {
                    $("#goback").hide();
                }
            });

            slide.find('#continue').click(function () {
                // this.i++;
                i = inc_i(1);
                if (i == 2) {
                    $("#goback").show();
                }

                if (i > 8) {
                    console.log(i)

                    slide.fadeOut($c.fade);
                    slideshow(2);
                    console.log('hey')
                };
            });
        }
        if (x == 2) {
            slide.fadeIn($c.fade);

            slide.find('#start').click(function () {
                CURRENTVIEW = new Comprehension();
            });
        }


    };
    var i = 1;

    var inc_i = function(x) {
        i += x;
        $(".tutorial").attr("src",'/static/images/instructions/tutorial' + i + '.png');
        return i
    }

    slideshow(1);

};



/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*****************
 *  COMPREHENSION CHECK QUESTIONS*
 *****************/

 var Comprehension = function(){

    var that = this; 

// Show the slide
$(".slide").hide();
$("#comprehension_check").fadeIn($c.fade);

    //disable button initially
    $('#comprehension').prop('disabled', true);

    //checks whether all questions were answered
    $('.demoQ').change(function () {
       if ($('input[name=team]:checked').length > 0 &&
         $('input[name=outcome]:checked').length > 0  &&
         $('input[name=goal]:checked').length > 0 )
       {
        $('#comprehension').prop('disabled', false)
    }else{
        $('#comprehension').prop('disabled', true)
    }
});

  $('#comprehension').click(function () {           
       var q1 = $('input[name=team]:checked').val();
       var q2 = $('input[name=outcome]:checked').val();
       var q3 = $('input[name=goal]:checked').val();

       // correct answers 
       answers = ["succeeded","failed","succeed"]

       if(q1 == answers[0] && q2 == answers[1] && q3 == answers[2]){
            // CURRENTVIEW = new TestPhase();
            CURRENTVIEW = new PredictionPhase();
       }else{
            $('input[name=team]').prop('checked', false);
            $('input[name=outcome]').prop('checked', false);
            $('input[name=goal]').prop('checked', false);
            CURRENTVIEW = new ComprehensionCheckFail();
       }
   });
}

/*****************
 *  COMPREHENSION FAIL SCREEN*
 *****************/

var ComprehensionCheckFail = function(){
// Show the slide
$(".slide").hide();
$("#comprehension_check_fail").fadeIn($c.fade);
$('#instructions-training-1-button').unbind();
$('#comprehension').unbind();

$('#comprehension_fail').click(function () {           
  CURRENTVIEW = new Instructions();
  $('#comprehension_fail').unbind();
   });
}

/*************************
 * PREDICTION PHASE
 *************************/

 var PredictionPhase = function(){
    var that = this;
    this.trialinfo;    

    this.init_trial = function () {
        if (STATE.index >= $c.predict.length) { //change here for debugging
            this.finish();
            return false;
        }

        // Load the new trialinfo
        this.trialinfo = $c.predict[STATE.index];
        // Update progress bar
        
        update_progress(STATE.index, $c.predict.length);
        return true;
    }; 


    this.display_stim = function (that) {

        if (that.init_trial()) {
            
            $('.prompt-text').html($c.predict_text);
            
            //show image 
            // $(".plinko_image").attr("src",'/static/images/plinko_predict_' + that.trialinfo.ID+ '.png');
            $(".hierarchy").attr("src",'/static/images/highlighted/highlighted' + that.trialinfo.ID + '.png');

            // Questions 
            var html = "" ; 
            for (var i=0; i<1; i++) {
                var q = $c.questions[0].q1[i] + that.trialinfo.cause + $c.questions[0].q2[i] + that.trialinfo.effect +  $c.questions[0].q3[i]  
                html += '<p class="question-' + i + '">' + q +'</p><div class="s-'+i+'"></div><div class="l-'+i+'"></div><br />' ;                
            }
            $('#predict_container').html(html) ;

            // # of sliders
            for (var i=0; i<1; i++) {
                // Create the sliders
                $('.s-'+i).slider().on("slidestart", function( event, ui ) {
                    // Show the handle
                    $(this).find('.ui-slider-handle').show() ;
                });
                $('.s-'+i).bind("slidestart", function( event, ui ) {
                    // Show the handle
                    $('#trial_next1').prop('disabled', false);
                });
                // Put labels on the sliders
                $('.l-'+i).append("<label style='width: 33%'>" +  $c.questions[0].l[0] + "</label>") ; 
                $('.l-'+i).append("<label style='width: 33%'></label>") ; 
                $('.l-'+i).append("<label style='width: 33%'>" + $c.questions[0].l[1] + "</label>") ;
            }

            // Hide all the slider handles 
            $('.ui-slider-handle').hide() ;               
            $('#trial_next1').prop('disabled', true);
        }       
    };

    this.record_response = function() {     
        response =  $('.s-0').slider('value');   
        
        psiTurk.recordTrialData([
            'id', this.trialinfo.ID, 
            'type', 'predict',
            'counterbalance', 'NA', 
            'prior',response]);


        STATE.set_index(STATE.index + 1);
        $('#trial_next1' ).show()
        
        // Update the page with the current phase/trial
        this.display_stim(this);
    };

    this.finish = function() {
        STATE.set_index(0); //resets the state variable 
        CURRENTVIEW = new JudgementPhase();
    };

    // Load the trial html page
    $(".slide").hide();

    // Show the slide
    var that = this; 
    $("#prediction").fadeIn($c.fade);
    $('#trial_next1.next').click(function () {
        that.record_response();
    });

    // Initialize the current trial
    if (this.init_trial()) {
        // Start the test
        this.display_stim(this) ;
    };
}

/*************************
 * Judgement PHASE
 *************************/

 var JudgementPhase = function(){
    var that = this;
    this.trialinfo;    
    this.init_trial = function () {
        if (STATE.index >= $c.judgement.length) { //change here for debugging
            this.finish();
            return false;
        }

        // Load the new trialinfo
        this.trialinfo = $c.judgement[STATE.index];
        // Update progress bar
        
        update_progress(STATE.index, $c.judgement.length);
        return true;
    }; 


    this.display_stim = function (that) {

        if (that.init_trial()) {
            
            $('.prompt-text').html($c.judgement_text);
            
            // $('.question-prompt').html("To what extent do you agree with the following statement?");

            flip = ['left','right']
            flipped = flip[Math.floor(Math.random() * 2)]

            //show image 
            $(".hierarchy").attr("src",'/static/images/situations/situation' + that.trialinfo.ID  + '.png');

            // Questions 
            var html = "" ; 
            for (var i=0; i<1; i++) {
                var q = $c.questions[1].q1[i] + that.trialinfo.cause + $c.questions[1].q2[i] + that.trialinfo.effect
                html += '<p class="question-' + i + '">' + q +'</p><div class="s-1"></div><div class="l-'+i+'"></div><br />' ;
            }
            $('#judgement_container').html(html) ;
            
                $('.s-1').slider().on("slidestart", function( event, ui ) {
                    $(this).find('.ui-slider-handle').show() ;
                    $('#trial_next2').prop('disabled', false);
                });

                // Put labels on the sliders
                $('.l-0').append("<label style='width: 33%'>" +  $c.questions[1].l[0] + "</label>") ; 
                $('.l-0').append("<label style='width: 33%'></label>") ;// + $c.questions[1].l[1] + "</label>") ; 
                $('.l-0').append("<label style='width: 33%'>" + $c.questions[1].l[2] + "</label>") ; 

            // Hide all the slider handles 
            $('.ui-slider-handle').hide() ;            
            $('#trial_next2').prop('disabled', true);
        }       
    };

    this.record_response = function() {     
        response =  $('.s-1').slider('value');   

        psiTurk.recordTrialData([
            'id', this.trialinfo.ID, 
            'type', 'judgement',
            'counterbalance', flipped, 
            'judgement',response]);


        STATE.set_index(STATE.index + 1);
        $('#trial_next2' ).show()
        
        // Update the page with the current phase/trial
        this.display_stim(this);
    };

    this.finish = function() {
        CURRENTVIEW = new Demographics();
    };

    // Load the trial html page
    $(".slide").hide();

    // Show the slide
    var that = this; 
    $("#judgement").fadeIn($c.fade);
    $('#trial_next2.next').click(function () {
        that.record_response();
    });

    // Initialize the current trial
    if (this.init_trial()) {
        // Start the test
        this.display_stim(this) ;
    };
}

/*****************
 *  DEMOGRAPHICS*
 *****************/

 var Demographics = function(){

    var that = this; 

// Show the slide
$(".slide").hide();
$("#demographics").fadeIn($c.fade);

    //disable button initially
    $('#trial_finish').prop('disabled', true);

    //checks whether all questions were answered
    $('.demoQ').change(function () {
       if ($('input[name=sex]:checked').length > 0 &&
         $('input[name=age]').val() != "")
       {
        $('#trial_finish').prop('disabled', false)
    }else{
        $('#trial_finish').prop('disabled', true)
    }
});

// deletes additional values in the number fields 
$('.numberQ').change(function (e) {    
    if($(e.target).val() > 100){
        $(e.target).val(100)
    }
});

this.finish = function() {
    debug("Finish test phase");

        // Show a page saying that the HIT is resubmitting, and
        // show the error page again if it times out or error
        var resubmit = function() {
            $(".slide").hide();
            $("#resubmit_slide").fadeIn($c.fade);

            var reprompt = setTimeout(prompt_resubmit, 10000);
            psiTurk.saveData({
                success: function() {
                    clearInterval(reprompt); 
                    finish();
                }, 
                error: prompt_resubmit
            });
        };

        // Prompt them to resubmit the HIT, because it failed the first time
        var prompt_resubmit = function() {
            $("#resubmit_slide").click(resubmit);
            $(".slide").hide();
            $("#submit_error_slide").fadeIn($c.fade);
        };

        // Render a page saying it's submitting
        psiTurk.showPage("submit.html") ;
        psiTurk.saveData({
            success: psiTurk.completeHIT, 
            error: prompt_resubmit
        });
    }; //this.finish function end 

    $('#trial_finish').click(function () {           
       var feedback = $('textarea[name = feedback]').val();
       var sex = $('input[name=sex]:checked').val();
       var age = $('input[name=age]').val();

       psiTurk.recordUnstructuredData('feedback',feedback);
       psiTurk.recordUnstructuredData('sex',sex);
       psiTurk.recordUnstructuredData('age',age);
       that.finish();
   });
};


// --------------------------------------------------------------------

/*******************
 * Run Task
 ******************/

 $(document).ready(function() { 
    // Load the HTML for the trials
    psiTurk.showPage("trial.html");

    // Record various unstructured data
    psiTurk.recordUnstructuredData("condition", condition);
    psiTurk.recordUnstructuredData("counterbalance", counterbalance);

    // Start the experiment
    STATE = new State();
    // Begin the experiment phase
    if (STATE.instructions) {
        // CURRENTVIEW = new JudgementPhase();
        CURRENTVIEW = new Instructions();
        // CURRENTVIEW = new PredictionPhase();
        // CURRENTVIEW = new Comprehension();

    }
});
