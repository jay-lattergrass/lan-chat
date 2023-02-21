// load data
async function load_name(){
	return await fetch("/get_user_name")
	.then(async function(response){
		return await response.json();
	})
	.then(async function(text){
		return text["user_name"];
	})
}

async function load_messages(){
	return await fetch("/get_all_messages")
	.then(async function(response){
		return await response.json();
	})
	.then(async function(text){
		return text;
	})
}

async function load_messages(){
	return await fetch("/get_all_messages")
	.then(async function(response){
		return await response.json();
	})
	.then(async function(text){
		return text;
	})
}

// add messages
async function add_message(value, scroll){
	let user = await load_name();
	let msg_div = $("#roomMessages");
	let html = "";

	if(value["user"] !== user){
		html += '<div class="p-2 d-flex justify-content-end"><div class="chat-message" id=msg-"' + value["id"] + '"><div class="row chat-message-user">' + value["user"] + '</div><div class="row chat-message-content">' + value["content"] + '</div><div class="row chat-message-date">' + value["created"] + '</div></div></div>';
	}
	else if(value["user"] === user){
		html += '<div class="p-2 d-flex justify-content-start"><div class="my-chat-message" id="msg-' + value["id"] + '"><div class="row my-message-user">' + value["user"] + '</div><div class="row my-message-content">' + value["content"] + '</div><div class="row my-message-date">' + value["created"] + '</div></div></div>';
	}

	msg_div.append(html);

	if(scroll){
		scrollToBottom();
	}
}

// socket settings
let socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("connect", async function(){
	$(document).on('submit', '#msgForm', async function(e){
		e.preventDefault();
		let content = $('#inputText').val();
		let user = await load_name();

		if(content === ""){
			return false; // don't submit empty strings
		}

		// clear input box
		$('#inputText').val("");

		socket.emit("insert_message", {
			"content": content,
			"user": user,
		});
	});
});

socket.on("message_response", async function(msg){
	add_message(msg, true);
});

window.onload = async function(){
	let scroll = false;
	let msgs = await load_messages();
	
	$.each(msgs, function(index, value){
		if(index === msgs.length - 1){
			scroll = true;
		}
		add_message(value, scroll);
	});
}

// TODO: Implement smooth scrolling
function scrollToBottom(){
	let objDiv = document.getElementById("roomMessages");
	objDiv.scrollTop = objDiv.scrollHeight;
}
