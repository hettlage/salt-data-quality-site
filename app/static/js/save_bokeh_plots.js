(function($) {
    $(document).ready(function() {
        $('button.save-plots').click(function() {
            var zip = new JSZip();

            $('figure.data-quality-item').each(function(index, element) {
                var exportName = $(element).attr('data-export-name');

                $('canvas.bk-canvas').each(function(index, element) {
                    var url = this.toDataURL("application/pdf");
                    zip.file(exportName + '.png', url.substr(url.indexOf(',') + 1), {base64: true});
                });
            });

            var content = zip.generate({type: 'blob'});
            console.log(zip);
            saveAs(content, 'plots.zip');
        });
    });
})(jQuery);


