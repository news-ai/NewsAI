var code = $.urlParam('code');

if (error !== '') {
    document.getElementById('error').style.display = 'block';
    document.getElementById('error').innerHTML = error;
}

if (unique_id !== '' || code) {
    var id = ''

    if (code !== '') {
        id = code;
    }

    if (unique_id !== '') {
        id = unique_id;
        var pageUrl = '?' + 'code=' + id;
        window.history.pushState('', '', pageUrl);
    }

    $.getJSON('/a/position/' + id, function(data) {
        document.getElementById('linePosition').innerHTML = data.position;
    });

    document.getElementById('twitter_link').setAttribute('data-url', 'https://www.newsai.org/?invite=' + id);
    document.getElementById('facebook_link').href = 'https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fwww.newsai.org%2F%3Finvite%3D' + id + '&amp;src=sdkpreparse';
    document.getElementById('subscribe').style.display = 'block';
} else {
    document.getElementById('check-position').style.display = 'block';
}