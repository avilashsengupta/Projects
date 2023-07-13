const now = new Date();
var hours, minutes, seconds;
function setClock()
{
	hours = now.getHours();
	minutes = now.getMinutes();
	seconds = now.getSeconds();
	string = '';
	if(parseInt(hours) < 10) string += '0' + hours + ':';
	else string += hours + ':';
	if(parseInt(minutes) < 10) string += '0' + minutes + ':';
	else string += minutes + ':';
	if(parseInt(seconds) < 10) string += '0' + seconds;
	else string += seconds;
	document.getElementById('current-time').innerHTML = string;
}
function showClock(hours, minutes, seconds)
{
	setClock();
	setInterval(runClock, 1000);
}
function runClock()
{
	seconds++;
	if(seconds == 60)
	{
		seconds = 0;
		minutes++;
		if(minutes == 60)
		{
			minutes = 0;
			hours++;
			if(hours == 24) hours = 0;
		}
	}
	string = '';
	if(parseInt(hours) < 10) string += '0' + hours + ':';
	else string += hours + ':';
	if(parseInt(minutes) < 10) string += '0' + minutes + ':';
	else string += minutes + ':';
	if(parseInt(seconds) < 10) string += '0' + seconds;
	else string += seconds;
	document.getElementById('current-time').innerHTML = string;
}
function togglePasswordView()
{
	let check = document.getElementById('add-usercode');
	if(check.type == 'password') check.type = 'text';
	else check.type = 'password';
}
