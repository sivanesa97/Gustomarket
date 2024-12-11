$(document).ready(function () {
    let choices = [
        "Bottled Day & Night",
        "Bottled Day & Night",
        "Bottled Day & Night",
        "Bottled Day & Night",
        "Bottled Day & Night"
    ];
    let $ = document;
    let list_group = $.querySelector(".list-group");

    var myproductimg = '<img src="assets/img/prod-img.png" alt="">';
    var myclose = '<img src="assets/img/close-icon.png" alt="">';
    let inputTxt = document.getElementById('inputTxt')


    function ListItemGenerator() {
        if (!inputTxt.value) {
            inputTxt.parentElement.classList.remove("active");
            list_group.style.display = "none";
        } else {
            inputTxt.parentElement.classList.add("active");
            list_group.style.display = "block";

            let SearchResults = choices.filter(function (choice) {
                return choice.toLowerCase().startsWith(inputTxt.value.toLowerCase());
            });

            CreatingList(SearchResults);

            function CreatingList(Words) {
                let createdList = Words.map(function (word) {
                    return "<li>" + myproductimg + "<span>" + word + "</span>" + myclose + "</li>";
                });
                let CustomListItem;
                if (!CreatingList.length) {
                    CustomListItem = "<li>" + inputTxt.value + "</li>";
                } else {
                    CustomListItem = createdList.join("");
                }
                list_group.innerHTML = CustomListItem;
                CompleteText();
            }
        }

        function CompleteText() {
            all_list_items = list_group.querySelectorAll("li");
            all_list_items.forEach(function (list) {
                list.addEventListener("click", function (e) {
                    inputTxt.value = e.target.textContent;
                    list_group.style.display = "none";
                });
            });
        }
    }

    inputTxt.addEventListener("keyup", ListItemGenerator);


    // --------------editor js --------------

    ClassicEditor
        .create(document.querySelector('.editor'))
        .catch(error => {
            return error
        });
    ClassicEditor
        .create(document.querySelector('.editor1'))
        .catch(error => {
            return error
        });




});

// --------------text tags js --------------
// (function ($) {

//     var methods = {
//         init: function (opts) {
//             opts = opts || {};
//             opts.tags = opts.tags || [];

//             var me = $(this);
//             var clean = new RegExp(',', 'g');
//             me.wrap('<div class="tag-cloud" />');
//             var cloud = me.parents('.tag-cloud');

//             cloud.click(function () {
//                 me.focus();
//             });

//             var addTag = function (value) {
//                 value = value.replace(clean, '');
//                 if (value !== '') {
//                     var tag = $('<div class="tag"><span>' + value + '</span></div>');
//                     var del = $('<a href="javascript:void(0)" class="close">Delete</a>');

//                     del.click(function () {
//                         del.parent().remove();
//                     });

//                     tag.append(del);
//                     tag.insertBefore(me);
//                 }
//             }

//             me.blur(function () {
//                 addTag(this.value);
//                 this.value = '';
//             });
//             me.keyup(function (e) {
//                 var key = e.keyCode;
//                 var isEnter = key == 13;
//                 var isComma = key == 188;
//                 var isBack = key == 8;

//                 if (isEnter || isComma) {
//                     addTag(this.value);
//                     this.value = '';
//                 }
//                 if (isBack && this.data('delete-prev')) {
//                     $(this).prev().remove();
//                     $(this).data('delete-prev', false);
//                 } else if (isBack && this.value === '') {
//                     $(this).data('delete-prev', true);

//                 }
//             });
//             $.each(opts.tags, function (i, e) {
//                 addTag(e);
//             });
//         },
//         get: function () {
//             return $('.tag span', this.parent()).map(function () {
//                 return $(this).text();
//             });
//         },
//         clear: function () {
//             $('div', this).remove();
//         }
//     };
//     $.fn.tagcloud = function (method) {
//         if (methods[method]) {
//             return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
//         } else if (typeof method === 'object' || !method) {
//             return methods.init.apply(this, arguments);
//         } else {
//             $.error('Method ' + method + ' does not exist on tagcloud plugin');
//         }
//     };
// })(jQuery);

// $('.tags').tagcloud({
//     tags: ['Tag Name']

// });
// var tags = $('.tags').tagcloud('get');



(function ($) {

    var methods = {
        init: function (opts) {
            opts = opts || {};
            opts.tags = opts.tags || [];

            var me = $(this);
            var clean = new RegExp(',', 'g');
            me.wrap('<div class="tag-cloud" />');
            var cloud = me.parents('.tag-cloud');

            cloud.click(function () {
                me.focus();
            });

            var addTag = function (value) {
                value = value.replace(clean, '');
                if (value !== '') {
                    var tag = $('<div class="tag"><span>' + value + '</span></div>');
                    var del = $('<a href="javascript:void(0)" class="close">Delete</a>');

                    del.click(function () {
                        del.parent().remove();
                        updateHiddenField();
                    });

                    tag.append(del);
                    tag.insertBefore(me);
                    updateHiddenField();
                }
            }

            var updateHiddenField = function () {
                var hiddenInput = cloud.find('.hidden-tags');
                if (!hiddenInput.length) {
                    hiddenInput = $('<input type="hidden" class="hidden-tags" name="product-tags" />');
                    cloud.append(hiddenInput);
                }
                // var tagValues = $('.tag span', cloud).map(function () {
                var tagValues = $('.tag span', cloud).not(':contains("Tag Name")').map(function () {
                    return $(this).text();
                }).get().join(',');
                hiddenInput.val(tagValues);
            };

            me.blur(function () {
                addTag(this.value);
                this.value = '';
            });
            me.keyup(function (e) {
                var key = e.keyCode;
                var isEnter = key == 13;
                var isComma = key == 188;
                var isBack = key == 8;

                if (isEnter || isComma) {
                    addTag(this.value);
                    this.value = '';
                }
                if (isBack && me.data('delete-prev')) {
                    me.prev().remove();
                    me.data('delete-prev', false);
                    updateHiddenField();
                } else if (isBack && this.value === '') {
                    me.data('delete-prev', true);
                }
            });
            $.each(opts.tags, function (i, e) {
                addTag(e);
            });
        },
        get: function () {
            return $('.tag span', this.parent()).map(function () {
                return $(this).text();
            });
        },
        clear: function () {
            $('div', this).remove();
            updateHiddenField();
        }
    };

    $.fn.tagcloud = function (method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on tagcloud plugin');
        }
    };
})(jQuery);

$('#product-tags').tagcloud({
    tags: ['Tag Name']
});
// var tags = $('.tags').tagcloud('get');


(function ($) {

    var methods = {
        init: function (opts) {
            opts = opts || {};
            opts.tags = opts.tags || [];

            var me = $(this);
            var clean = new RegExp(',', 'g');
            me.wrap('<div class="tag-cloud" />');
            var cloud = me.parents('.tag-cloud');

            cloud.click(function () {
                me.focus();
            });

            var addTag = function (value) {
                value = value.replace(clean, '');
                if (value !== '') {
                    var tag = $('<div class="tag"><span>' + value + '</span></div>');
                    var del = $('<a href="javascript:void(0)" class="close">Delete</a>');

                    del.click(function () {
                        del.parent().remove();
                        updateHiddenField();
                    });

                    tag.append(del);
                    tag.insertBefore(me);
                    updateHiddenField();
                }
            }

            var updateHiddenField = function () {
                var hiddenInput = cloud.find('.hidden-tags');
                if (!hiddenInput.length) {
                    hiddenInput = $('<input type="hidden" class="hidden-tags" name="product-attributes" />');
                    cloud.append(hiddenInput);
                }
                // var tagValues = $('.tag span', cloud).map(function () {
                var tagValues = $('.tag span', cloud).not(':contains("Tag Name")').map(function () {
                    return $(this).text();
                }).get().join(',');
                hiddenInput.val(tagValues);
            };

            me.blur(function () {
                addTag(this.value);
                this.value = '';
            });
            me.keyup(function (e) {
                var key = e.keyCode;
                var isEnter = key == 13;
                var isComma = key == 188;
                var isBack = key == 8;

                if (isEnter || isComma) {
                    addTag(this.value);
                    this.value = '';
                }
                if (isBack && me.data('delete-prev')) {
                    me.prev().remove();
                    me.data('delete-prev', false);
                    updateHiddenField();
                } else if (isBack && this.value === '') {
                    me.data('delete-prev', true);
                }
            });
            $.each(opts.tags, function (i, e) {
                addTag(e);
            });
        },
        get: function () {
            return $('.tag span', this.parent()).map(function () {
                return $(this).text();
            });
        },
        clear: function () {
            $('div', this).remove();
            updateHiddenField();
        }
    };

    $.fn.tagcloud = function (method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on tagcloud plugin');
        }
    };
})(jQuery);

$('#product-attributes').tagcloud({
    tags: ['Tag Name']
});