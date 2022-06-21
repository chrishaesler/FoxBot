const chatbot = function () {
	return {
		index: 0,
		chatTimeout: 10000,
		chatTimer: false,

		init: function () {
			$("#chat-submit").click(function (e) {
				e.preventDefault();
				let msg = $("#chat-input").val();

				if (msg.trim() == '') {
					return false;
				}

				chatbot.generateMessage(msg)
			});

			$("#chat-circle, .chat-box-toggle").click(function () {
				$("#chat-circle").toggle();
				$(".chat-box").toggle();
			})

			chatbot.
			
			
			
			({}, "chat_start", function (data, textStatus, jqXHR) {
				let answer = data

				answer["answers"].forEach(function (item) {
					chatbot.buildMessage(item, 'user')
				});
			})
		},

		generateMessage: function (msg, request = false) {
			let message = {}
			let type = "chat_answer";

			if (request === undefined) {
				request = false
			}

			if (msg != "") {
				chatbot.buildMessage(msg, 'self')
				message = {
					"msg": msg
				}
			}

			if (request) {
				type = "chat_request";
			}

			chatbot.chatRequest(message, type, function (data, textStatus, jqXHR) {
				let answer = data

				answer["answers"].forEach(function (item) {
					chatbot.buildMessage(item, 'user')
				});

				switch (answer.state) {

					case "chat_end":
						chatbot.chatTimer = window.setTimeout(function () {
							chatbot.generateMessage("", true);
							window.clearTimeout(chatbot.chatTimer);
							chatbot.chatTimer = false
						}, chatbot.chatTimeout)

						break;

					case "chat_answer":
						if (chatbot.chatTimer) {
							window.clearTimeout(chatbot.chatTimer);
							chatbot.chatTimer = false
						}

						break;
				}
			})
		},

		buildMessage: function (message, type) {
			chatbot.index++;

			let str = '<div id="cm-msg-%INDEX%" class="chat-msg %TYPE%"><span class="msg-avatar"><img src="%IMAGELINK%"></span><div class="cm-msg-text">%MESSAGE%</div></div>';

			str = str.replace("%INDEX%", chatbot.index);
			str = str.replace("%TYPE%", type);
			str = str.replace("%MESSAGE%", message);
			if (type === 'self') {
				str = str.replace("%IMAGELINK%", "https://www.gravatar.com/avatar/b932e833a535ac1a345021333f7759bf?s=140&d=retro")
			} else {
				str = str.replace("%IMAGELINK%", "https://de.gravatar.com/userimage/203455495/3270fb2a3b3b13a75945a24ce3bcfd1d.png?size=200")
			}

			$(".chat-logs").append(str);
			$("#cm-msg-" + chatbot.index).hide().fadeIn(300);

			if (type == 'self') {
				$("#chat-input").val('');
			}

			$(".chat-logs").stop().animate({
				scrollTop: $(".chat-logs")[0].scrollHeight
			}, 1000);
		},

		chatRequest: function (data, type, callbackSuccess) {
			let endpointUrl = ""
			let methodType = ""

			switch (type) {
				case "chat_start":
					endpointUrl = "/init_chat";
					methodType = "GET";
					break;

				case "chat_request":
					endpointUrl = "/request_chat";
					methodType = "GET";
					break;

				case "chat_answer":
					endpointUrl = "/get_chat";
					methodType = "POST";
					break;
			}

			$.ajax({
				url: endpointUrl,
				type: methodType,
				data: data,
				success: callbackSuccess,
				error: function (jqXHR, textStatus, errorThrown) {

				}
			});
		}
	}
}();
$(document).ready(chatbot.init);
