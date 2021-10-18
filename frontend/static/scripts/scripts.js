window.onload = function () {
    $('#burger-button').click(function() {
        $('.nav-list').toggleClass('nav-show');
        $('body').toggleClass('body-overflow-hidden');
    });

    $('#btn-night-mode').click(function() {
        $('.wrapper').toggleClass('night-mode');        
        var mode;
        if ($(this).children().hasClass('fa-moon-o')){
            $(this).children().removeClass('fa-moon-o');
            $(this).children().addClass('fa-sun-o');
            mode = 'night';
        }else{
            $(this).children().addClass('fa-moon-o');
            $(this).children().removeClass('fa-sun-o');
            mode = 'day';
        }
        localStorage.setItem('night-mode', mode)        
    });

    $(function() {
        var mode = localStorage.getItem('night-mode');    
        
        if (mode === 'night'){
            $('#btn-night-mode').children().removeClass('fa-moon-o');
            $('#btn-night-mode').children().addClass('fa-sun-o');
            $('.wrapper').addClass('night-mode');
        } 
        if (mode === 'day'){
            $('#btn-night-mode').children().addClass('fa-moon-o');
            $('#btn-night-mode').children().removeClass('fa-sun-o');
            $('.wrapper').removeClass('night-mode');        
        }
    });

    $('.slider-popular-posts').slick({
        infinite: true,
        autoplay: true,
        autoplaySpeed: 7500,
        arrows: false,
        dots: true,
        slidesToShow: 3,
        slidesToScroll: 3,
        responsive: [
            {
                breakpoint: 1020,
                settings: {
                    arrows: false,
                    centerMode: true,
                    centerPadding: '25px',
                    slidesToShow: 2,
                    slidesToScroll: 2
                }
            },
            {
                breakpoint: 768,
                settings: {
                    arrows: false,
                    centerMode: true,
                    centerPadding: '15px',
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 350,
                settings: {
                    arrows: false,
                    centerMode: false,
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });
}