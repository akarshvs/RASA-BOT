$(document).ready(function () {
  var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
	//Widget Code
	var bot = '<div class="chatCont" id="chatCont">' +
	'<div class="micContain"><div class="micloader"> <div class="lds-ripple"><div></div><div></div></div></div></div>'+
		'<div class="bot_profile">' +
		'</div><!--bot_profile end-->' +
		'<div id="result_div" class="resultDiv"></div>' +
		'<div class="chatForm" id="chat-div">' +
		'<div class="spinner">' +
		'<div class="bounce1"></div>' +
		'<div class="bounce2"></div>' +
		'<div class="bounce3"></div>' +
		'</div>' +
		'<div><input type="text" id="chat-input" autocomplete="off" placeholder="Start Typing here..."' + 'class="form-control bot-txt"/>' +
		'<img src="mike.svg" class="mic" ></div></div>' +
		'</div><!--chatCont end-->' +

		'<div class="procontain"><div class="profile_div">' +
		'<div class="row">' +
		'<div class="col-hgt col-sm-offset-2">' +
		'<img src="bot.jpeg" class="img-circle img-profile">' +
		'</div><!--col-hgt end-->' +
		'<div class="col-hgt">' +
		'<div class="chat-txt">' +
		'' +
		'</div>' +
		'</div><!--col-hgt end-->' +
		'</div><!--row end--> </div> ' +
		'<div class="close">' +
		'<img src="close.svg"/>' +
		'</div>' +
		'</div><!--profile_div end-->';

		/*
		 * Check for browser support
		 */
		var supportMsg = document.getElementById('msg');
    var recognition = new SpeechRecognition();
    navigator.mediaDevices.getUserMedia({audio:true});
		recognition.lang = 'en-US';
		if ('speechSynthesis' in window) {
			console.log("Your browser supports.");
		} else {
		console.log("Your browser not supported ");
		}



		function speak(text) {
		  // Create a new instance of SpeechSynthesisUtterance.
			var msg = new SpeechSynthesisUtterance();

		  // Set the text.
			msg.text = text;

		  // Set the attributes

		  // If a voice has been selected, find the voice and set the
		  // utterance instance's voice attribute.
         console.log("done");
				voices = window.speechSynthesis.getVoices();
				msg.voice=voices[5];
        console.log("done");
		  // Queue this utterance.
			window.speechSynthesis.speak(msg);
		}


		// Set up an event listener for when the 'speak' button is clicked.


	$("mybot").html(bot);
  speak(" ");
	// ------------------------------------------ Toggle chatbot -----------------------------------------------
	$('.profile_div').click(function () {

		$('.close').fadeToggle(function(){
			$('.close').css("transform","rotate(0deg)");
		});
		$('.profile_div').fadeToggle();
		$('.chatCont').fadeToggle(
			function(){
				$('.chatCont').css("opacity","1");
				$('.chatCont').css("bottom","165px");
			}
		);
		$('.bot_profile').fadeToggle();
		$('.chatForm').fadeToggle();
		document.getElementById('chat-input').focus();
	});

	$('.close').click(function () {
		$('.close').fadeToggle(function(){
			$('.close').css("transform","rotate(-180deg)");
		});
		$('.profile_div').fadeToggle(
			function(){

			}
		);
		$('.chatCont').fadeToggle(
			function(){
				$('.chatCont').css("opacity","0.9");
				$('.chatCont').css("bottom","135px");
			}
		);
		$('.bot_profile').fadeToggle();
		$('.chatForm').fadeToggle();
	});

	$('.mic').click(function(){
		$('.micContain').fadeToggle();
		recognition.start();
	})
	recognition.onresult = function(event) {
	  	$('.micContain').fadeToggle();
			var vres = event.results[0][0].transcript;
			setUserResponse(vres);
			send(vres);

	}


	// on input/text enter--------------------------------------------------------------------------------------
	$('#chat-input').on('keyup keypress', function (e) {
		var keyCode = e.keyCode || e.which;
		var text = $("#chat-input").val();
		if (keyCode === 13) {
			if (text == "" || $.trim(text) == '') {
				e.preventDefault();
				return false;
			} else {
				$("#chat-input").blur();
				setUserResponse(text);
				send(text);
				e.preventDefault();
				return false;
			}
		}
	});


	//------------------------------------------- Call the RASA API--------------------------------------
	function send(text) {


		$.ajax({
			url: 'http://localhost:5002/webhooks/rest/webhook', //  RASA API
			type: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			data: JSON.stringify({
				"sender": "user",
				"message": text
			}),
			success: function (data, textStatus, xhr) {
				console.log(data);

				if (Object.keys(data).length !== 0) {
					for (i = 0; i < Object.keys(data[0]).length; i++) {
						if (Object.keys(data[0])[i] == "buttons") { //check if buttons(suggestions) are present.
							addSuggestion(data[0]["buttons"])
						}

					}
				}



				setBotResponse(data);

			},
			error: function (xhr, textStatus, errorThrown) {
				console.log('Error in Operation');
				setBotResponse('error');
			}
		});





	}


	//------------------------------------ Set bot response in result_div -------------------------------------
	function setBotResponse(val) {
		setTimeout(function () {
            text = "";
			var converter = new showdown.Converter();
			if ($.trim(val) == '' || val == 'error') { //if there is no response from bot or there is some error

				val = 'Sorry I wasn\'t able to understand your Query. Let\'s try something else!'
				var BotResponse = '<p class="botResult">' + val + '</p><div class="clearfix"></div>';
				$(BotResponse).appendTo('#result_div');
				
			} else {

				//if we get message from the bot succesfully
				var msg = "";
				for (var i = 0; i < val.length; i++) {
					if (val[i]["image"]) { //check if there are any images
						msg += '<p class="botResult"><img  width="200" height="124" src="' + val[i].image + '/"></p><div class="clearfix"></div>';
					} else {
   
	                				
			            text =  val[i].text;
									html   = converter.makeHtml(text);
									console.log(html)
									msg += '<div class="botResult">' + html + '</div><div class="clearfix"></div>';
					
				}
					}

				

				BotResponse = msg;
				$(BotResponse).appendTo('#result_div');
                $('#result_div').find('a').attr("target","_blank"); 
				console.log(val);
			}
			scrollToBottomOfResults();
			hideSpinner();
			var readtxt=$('.botResult:last').text();
			  speak(readtxt);
		}, 500);
	}


	//------------------------------------- Set user response in result_div ------------------------------------
	function setUserResponse(val) {
		var UserResponse = '<p class="userEnteredText">' + val + '</p><div class="clearfix"></div>';
		$(UserResponse).appendTo('#result_div');
		$("#chat-input").val('');
		scrollToBottomOfResults();
		showSpinner();
		$('.suggestion').remove();
	}


	//---------------------------------- Scroll to the bottom of the results div -------------------------------
	function scrollToBottomOfResults() {
		var terminalResultsDiv = document.getElementById('result_div');
		terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
	}


	//---------------------------------------- Spinner ---------------------------------------------------
	function showSpinner() {
		$('.spinner').show();
	}

	function hideSpinner() {
		$('.spinner').hide();
	}




	//------------------------------------------- Buttons(suggestions)--------------------------------------------------
	function addSuggestion(textToAdd) {
		setTimeout(function () {
			var suggestions = textToAdd;
			var suggLength = textToAdd.length;
			$('<p class="suggestion"></p>').appendTo('#result_div');
			// Loop through suggestions
			for (i = 0; i < suggLength; i++) {
				$('<span class="sugg-options">' + suggestions[i].title + '</span>').appendTo('.suggestion');
			}
			scrollToBottomOfResults();
		}, 1000);
	}


	// on click of suggestions get value and send to API.AI
	$(document).on("click", ".suggestion span", function () {
		var text = this.innerText;
		setUserResponse(text);
		send(text);
		$('.suggestion').remove();
	});
	// Suggestions end -----------------------------------------------------------------------------------------


});
