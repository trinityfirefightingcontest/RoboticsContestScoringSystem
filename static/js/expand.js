$(document).ready(function() {
	$('#candleLocationImg').on('click', function() {
		if ($(this).height() === 300) {
			$(this).animate({height: '500px', width: '500px'});
			$('#buttonPanel').attr('class', 'col-lg-6');
			$('#addRunOptions').attr('class', 'col-lg-6');
		}
		else {
			$(this).animate({height: "300px", width: "300px"});
			$('#buttonPanel').attr('class', 'col-lg-4');
			$('#addRunOptions').attr('class', 'col-lg-8');
		}
	});

	$('#puppyLocationImg').on('click', function() {
		if ($(this).height() === 300) {
			$(this).animate({height: '500px', width: '500px'});
			$('#buttonPanel').attr('class', 'col-lg-6');
			$('#addRunOptions').attr('class', 'col-lg-6');
		}
		else {
			$(this).animate({height: "300px", width: "300px"});
			$('#buttonPanel').attr('class', 'col-lg-4');
			$('#addRunOptions').attr('class', 'col-lg-8');
		}
	});

	$('#startOrientImg').on('click', function() {
		if ($(this).height() === 150) {
			$(this).animate({height: '300px', width: '300px'});
			$('#buttonPanel').attr('class', 'col-lg-6');
			$('#addRunOptions').attr('class', 'col-lg-6');
		}
		else {
			$(this).animate({height: '150px', width: '150px'});
			$('#buttonPanel').attr('class', 'col-lg-4');
			$('#addRunOptions').attr('class', 'col-lg-8');
		}
	});

	$('#roomImg').on('click', function() {
		if ($(this).height() == 500) {
			$(this).animate({height:'600px', width: '500px'});
			$('#buttonPanel').attr('class', 'col-lg-6');
			$('#addRunOptions').attr('class', 'col-lg-6');	
		} 
		else {
			$(this).animate({height: '500px', width: '350px'});
			$('#buttonPanel').attr('class', 'col-lg-4');
			$('#addRunOptions').attr('class', 'col-lg-8');
		}
	});

	$('#furnitureLocationImg').on('click', function() {
		if ($(this).height() === 300) {
			$(this).animate({height: '500px', width: '500px'});
			$('#buttonPanel').attr('class', 'col-lg-6');
			$('#addRunOptions').attr('class', 'col-lg-6');
		}
		else {
			$(this).animate({height: '300px', width: '300px'});
			$('#buttonPanel').attr('class', 'col-lg-4');
			$('#addRunOptions').attr('class', 'col-lg-8');
		}
	});	

	$('#babyLocationImg').on('click', function() {
		if ($(this).height() == 300) {
			$(this).animate({height: '500px', width: '500px'});
			$('#buttonPanel').attr('class', 'col-lg-6');
			$('#addRunOptions').attr('class', 'col-lg-6');
		}
		else {
			$(this).animate({height: '300px', width: '300px'});
			$('#buttonPanel').attr('class', 'col-lg-4');
			$('#addRunOptions').attr('class', 'col-lg-8');
		}
	});
});
