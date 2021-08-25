function login() {
	var username = document.getElementById("ID").value;
	var password = document.getElementById("PASSWORD").value;
	if(username == "") {
		$.jGrowl("用户名不能为空！", {
			header: '提醒'
		});
	} else if(password == "") {
		$.jGrowl("验证码不能为空！", {
			header: '提醒'
		});
	} else {
		AjaxFunc();
	}
}

function AjaxFunc() {
	var username = document.getElementById("ID").value;
	var password = document.getElementById("PASSWORD").value;
	var aurl = window.localStorage.getItem('baseUrl') + '/conservator/manager_login';
	var adic = {
		"request": {
			"encrypt_type": "",
			"token": ""
		},
		"body": {
			phone: username,
			captcha: password
		}
	}
	$.ajax({
		type: 'POST',
		url: aurl,
		dataType: "json",
		data: JSON.stringify(adic),
		success: function(data) {
			console.log(data)

		},
		error: function(xhr, type) {
			console.log(xhr);
		}
	});
}
var time;
	window.localStorage.setItem('baseUrl2', 'http://119.27.169.84:19001')

$('#getCode').click(function() {

	var aurl = window.localStorage.getItem('baseUrl2') + '/runningman/send_captcha';
	var username = document.getElementById("ID").value;

	var adic = {
		"request": {
			"encrypt_type": "",
			"token": ""
		},
		"body": {
			phone: username,
			type: 3
		}
	}
	$.ajax({
		type: 'POST',
		url: aurl,
		dataType: "json",
		data: JSON.stringify(adic),
		success: function(data) {
			console.log(data)
//			{"response": {"retcode": 0, "message": "\u8bf7\u6c42\u6210\u529f"}, "body": {}}
alert(JSON.stringify(data))
			if(data.response.retcode==0){
				$(this).text('已发送短信' + '（' + count + '）');
			$('#getCode').css('background', 'lightgrey');
			$('#getCode').attr('disabled', 'disabled');
			$(this).attr('disabled', 'disabled');
			time = self.setInterval("clock()", 1000);
			}else{
				alert(data.response.message);
			}
			
			console.log(time)
		},
		error: function(xhr, type) {
			console.log(xhr);
		}
	});

})

var count = 120;

function clock() {
	count = count - 1;
	$('#getCode').text('已发送短信' + '（' + count + '）');
	if(count == 0) {
		console.log(time)
		time = clearInterval(time);
		console.log(time)
		$('#getCode').css('background', '#e7a15f');
		$('#getCode').removeAttr('disabled');
		$('#getCode').text('获取验证码');
		count = 3;

	}
}