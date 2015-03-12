$(function() {
    $(window).resize(function() {
        // These should refer to left panel and right panel
        var $sidePanel = $('.side-panel');
        var $centralPanel = $('.central-panel');
        // FIX THIS
        if (Math.max($sidePanel.height(), $centralPanel.height()) < $(window).height()) {
            $($sidePanel).height($(window).height() - $($sidePanel).offset().top);
            $($centralPanel).height($(window).height() - $($centralPanel).offset().top);
        }
    });
    $(window).resize();
});
