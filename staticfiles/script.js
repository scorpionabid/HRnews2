// Saytın tam yüklənməsini gözləyirik
$(document).ready(function () {
    // 1. Telefon və planşet ölçülərində main content sectionun gizlədilməsi
    function hideMainContentOnMobile() {
        if ($(window).width() < 768) { // 768px-dən kiçik ekranlarda
            $('main .col-lg-8').hide(); // Əsas məzmunu gizlət
        } else {
            $('main .col-lg-8').show(); // Geniş ekranda yenidən göstər
        }
    }

    // İlk olaraq yüklənəndə yoxlayırıq
    hideMainContentOnMobile();

    // Ekran ölçüsü dəyişdikdə funksiyanı yenidən işə salırıq
    $(window).resize(function () {
        hideMainContentOnMobile();
    });

    // 2. Subkateqoriyaların hover edildikdə görünməsi
    $('.dropdown').hover(function () {
        $(this).find('.dropdown-menu').stop(true, true).slideDown(200); // Subkateqoriyalar görünür
    }, function () {
        $(this).find('.dropdown-menu').stop(true, true).slideUp(200); // Subkateqoriyalar gizlənir
    });

    // 3. Xəbərlər dinamik əlavə olunduqda: köhnə xəbər aşağı düşür
    let newsCounter = 1; // Xəbər başlıqları sırasını təyin etmək üçün counter

    function addNews(title, hook, category, date) {
        // Köhnə xəbərləri aşağı köçürmək
        let previousNews1 = $('#news1').html();
        let previousNews2 = $('#news2').html();

        $('#news2').html(previousNews1); // Xəbər başlığı 2-ə köhnə xəbər köçürülür
        $('#additional-news').prepend(`
            <div class="col-md-4">
                <div class="card">
                    <img src="https://via.placeholder.com/600x400" class="card-img-top img-fluid" alt="Xəbər Şəkli">
                    <div class="card-body">
                        <h5 class="card-title"><a href="#">${previousNews2}</a></h5>
                    </div>
                </div>
            </div>
        `); // Əlavə xəbərlər bölməsinə köçürülən xəbər

        // Yeni xəbəri "Xəbər Başlığı 1"-ə yerləşdirmək
        $('#news1').html(`
            <h5 class="card-title"><a href="#">${title}</a></h5>
            <p class="card-text">${hook}</p>
            <p class="category">${category}</p>
            <p class="date">${date}</p>
            <div class="share">
                <a href="#"><i class="fab fa-facebook"></i></a>
                <a href="#"><i class="fab fa-twitter"></i></a>
                <a href="#"><i class="fab fa-linkedin"></i></a>
            </div>
        `);
    }

    // Xəbər əlavə etmək üçün düymə
    $('#add-news').on('click', function () {
        let title = `Xəbər Başlığı ${newsCounter}`;
        let hook = 'Bu, yenicə əlavə olunan xəbər üçün hook cümləsidir.';
        let category = 'Kateqoriya: Əsas Xəbərlər';
        let date = new Date().toLocaleDateString();

        addNews(title, hook, category, date); // Xəbəri əlavə etmək
        newsCounter++; // Növbəti xəbər üçün counter artırmaq
    });

    // 4. Əməkdaş şirkətlərin loqolarına hover animasiyası
    $('.partners-section img').hover(function () {
        $(this).css({
            'transform': 'scale(1.1)',
            'transition': 'all 0.3s ease'
        }); // Loqo hover edildikdə böyüyür
    }, function () {
        $(this).css('transform', 'scale(1)'); // Normal ölçüyə qayıdır
    });

    // 5. Hərəkət edən xəbər lentinin dinamikliyi
    function animateTicker() {
        $('.ticker').css('transform', 'translateX(100%)'); // Lentə əvvəlki mövqe verilir
        $('.ticker').animate({
            transform: 'translateX(-100%)' // Lent soldan sağa hərəkət edir
        }, 15000, 'linear', function () {
            animateTicker(); // Sonsuz döngü ilə yenidən animasiya
        });
    }
    animateTicker();

    // 6. Xəbər paylaşma linklərinin sosial media ilə inteqrasiyası
    $('.share a').on('click', function (e) {
        e.preventDefault();
        let platform = $(this).find('i').attr('class').split(' ')[1];
        let url = window.location.href;
        let title = $(this).closest('.card').find('.card-title').text();

        // Müxtəlif sosial media platformaları üçün link yaratmaq
        let shareUrl = '';
        if (platform === 'fa-facebook') {
            shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}&t=${title}`;
        } else if (platform === 'fa-twitter') {
            shareUrl = `https://twitter.com/intent/tweet?text=${title}&url=${url}`;
        } else if (platform === 'fa-linkedin') {
            shareUrl = `https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}`;
        }

        // Yeni pəncərədə paylaşım səhifəsi açılır
        window.open(shareUrl, '_blank', 'width=600,height=400');
    });

    // 7. Xəbər kartlarına hover effekti
    $('.card').hover(function () {
        $(this).css({
            'box-shadow': '0 8px 16px rgba(0, 123, 255, 0.3)',
            'transform': 'scale(1.02)',
            'transition': 'all 0.3s ease'
        }); // Hover effekti zamanı kölgə və ölçü dəyişir
    }, function () {
        $(this).css({
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'transform': 'scale(1)'
        }); // Normala qayıdır
    });

    // 8. Dinamik xəbər başlığı animasiyası
    function animateNewsTitles() {
        let newsCards = $('.card-title');
        let delay = 0;

        newsCards.each(function () {
            $(this).delay(delay).fadeIn(500).fadeOut(500).fadeIn(500); // Başlıq fade-in və fade-out effekti ilə göstərilir
            delay += 500;
        });
    }

    animateNewsTitles(); // İlk yüklənəndə başlıqlar animasiya olunur

    // 9. Elan kartları hover olduqda vurğulama
    $('.advertisement .card').hover(function () {
        $(this).css({
            'border': '2px solid #007bff',
            'transition': 'border 0.3s ease'
        }); // Elan hover edildikdə vurğulanır
    }, function () {
        $(this).css('border', 'none'); // Normala qayıdır
    });

    // 10. Back-to-top düyməsi
    $('body').append('<div id="back-to-top" style="position: fixed; bottom: 20px; right: 20px; display: none; background-color: #007bff; color: #fff; padding: 10px 15px; cursor: pointer; border-radius: 5px;">Yuxarı</div>');

    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('#back-to-top').fadeIn(); // 300px aşağıya düşüldükdə düymə görünür
        } else {
            $('#back-to-top').fadeOut(); // Yenidən yuxarı çıxdıqda gizlənir
        }
    });

    $('#back-to-top').on('click', function () {
        $('html, body').animate({ scrollTop: 0 }, 800); // Yuxarıya sürətli hərəkət
        return false;
    });
});
