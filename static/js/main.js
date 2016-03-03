require.config({baseUrl: "/static/js",
    shim: {
        'jquery': {
            exports: '$'
        }
    },

    paths: {
        "jquery": "//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min",
        "lodash": "//cdnjs.cloudflare.com/ajax/libs/lodash.js/2.2.1/lodash",
        "datejs": "//cdnjs.cloudflare.com/ajax/libs/datejs/1.0/date.min",
    }
});

require(["ui/spotlighter"],

        function(spotlighter) {
            spotlighter
                .initialize("#spotlight", "#jobs", "#show-all");

            $("#main").css("visibility", "visible");
        });