$(document).ready(function () {
    $("#manageteam-table .dropdown .btn").click(function () {
        if ($(this).hasClass('show')) {
            $("#manageteam-table").parent(".col-sm-12").addClass("hide-scroll");
        }
        else {
            $("#manageteam-table").parent(".col-sm-12").removeClass("hide-scroll");
        }

    });
});

//side bar menu orgnization chart page with active state class js start here
var mainMenuLinks = document.querySelectorAll(".menu-nav ul.menu-list li.menu-item");
mainMenuLinks.forEach((getEle, index) => {
    getEle.addEventListener("click", () => {
        sessionStorage.setItem("linkIndex", index);
    });

    var linksSetGet = JSON.parse(sessionStorage.getItem('linkIndex'));
    if (linksSetGet === index) {
        getEle.classList.add("is-active");
    }
});

var submenuLinks = document.querySelectorAll("ul.menu-list li.menu-item ul.menu-submenu li a");
submenuLinks.forEach((getElem, index) => {
    getElem.addEventListener("click", () => {
        sessionStorage.setItem("tabIndex", index);
    });
    var linkSetGet = JSON.parse(sessionStorage.getItem('tabIndex'));
    if (linkSetGet === index) {
        getElem.classList.add("tabactive");
    }
});

$(document).ready(function () {

    // --------------eye icon show and hide password--------------
    // $(function () {

    //     $('#eye').click(function () {

    //         if ($(this).hasClass('far fa-eye-slash')) {

    //             $(this).removeClass('far fa-eye-slash');

    //             $(this).addClass('far fa-eye');

    //             $('#password').attr('type', 'text');

    //         } else {

    //             $(this).removeClass('far fa-eye');

    //             $(this).addClass('far fa-eye-slash');

    //             $('#password').attr('type', 'password');
    //         }
    //     });
    // });

    // $(function () {

    //     $('#eye1').click(function () {

    //         if ($(this).hasClass('far fa-eye-slash')) {

    //             $(this).removeClass('far fa-eye-slash');

    //             $(this).addClass('far fa-eye');

    //             $('#confirm_password').attr('type', 'text');

    //         } else {

    //             $(this).removeClass('far fa-eye');

    //             $(this).addClass('far fa-eye-slash');

    //             $('#confirm_password').attr('type', 'password');
    //         }
    //     });
    // });
    $(function () {
        $('#eye').click(function () {
            togglePasswordVisibility('#password', this);
        });

        $('#eye1').click(function () {
            togglePasswordVisibility('#confirm_password', this);
        });
    
        $('#eye2').click(function () {
            togglePasswordVisibility('#new_password', this);
        });
    
        function togglePasswordVisibility(inputId, eyeIcon) {
            if ($(eyeIcon).hasClass('far fa-eye-slash')) {
                $(eyeIcon).removeClass('far fa-eye-slash');
                $(eyeIcon).addClass('far fa-eye');
                $(inputId).attr('type', 'text');
            } else {
                $(eyeIcon).removeClass('far fa-eye');
                $(eyeIcon).addClass('far fa-eye-slash');
                $(inputId).attr('type', 'password');
            }
        }
    });
    // --------------select drop down tooltip js--------------
    $('.tooltip-select').selectpicker({
        liveSearch: true
    }).on('loaded.bs.select', function (e) {

        var $el = $(this);

        var selectpickerData = $el.data('selectpicker');

        if (selectpickerData) {
            var $lis = selectpickerData.selectpicker.main.elements;

            $($lis).each(function (i) {
                var tooltip_title = $el.find('option').eq(i).attr('title');

                $(this).tooltip({
                    'title': tooltip_title || '',
                    'placement': 'left'
                });
            });
        }
    });


    // --------------data table js--------------

    $('#addteam-table').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false,
        visible: false,
    });

    $('#manageteam-table').DataTable({
        info: false,
        ordering: false,
        paging: false,
        responsive: false,
        "searching": false,
    });
    $('#managelocation-table').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#add-another-table').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#product-tables').DataTable({
        info: false,
        paging: false,
        "searching": false
    });
    $('#card-tables').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#card-tables1').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#purchasedprod-tables').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#prodsales-table').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });

    $('#transitprodt-tables').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });

    $('#deliveredprod-tables').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#creditsrequests-table').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#closerequests-table').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#currentblance-table').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#transactions-table').DataTable({
        info: false,
        paging: false,
        "searching": false
    });
    $('#customerlists-table').DataTable({
        info: false,
        paging: false,
        "searching": false
    });
    $('#purchaseodr-table').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#purchasehis-table').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#purchasehis-table1').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#purchasehis-table2').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });
    $('#purchasehis-table3').DataTable({
        info: false,
        ordering: false,
        paging: false,
        "searching": false
    });



    //--------------filter drop down--------------
    $(".filter-click").click(function (e) {
        $(".filter-dropdown-show").toggle();
        e.stopPropagation();
    });
    // $(".filter-dropdown-show").click(function (e) {
    //     e.stopPropagation();
    // });
    // $(document).click(function (e) {
    //     $(".filter-dropdown-show").hide();
    // });

    $(".filter-cliking").click(function (e) {
        $(".dash-filter-show").toggle();
        e.stopPropagation();
    });
    $(".dash-filter-show").click(function (e) {
        e.stopPropagation();
    });
    $(document).click(function (e) {
        $(".dash-filter-show").hide();
    });

    //--------------Advance Tabs wizard--------------
    $(".next").click(function () {
        const nextTabLinkEl = $(".nav-tabs .active")
            .closest("li")
            .next("li")
            .find("a")[0];
        const nextTab = new bootstrap.Tab(nextTabLinkEl);
        nextTab.show();
    });

    $(".previous").click(function () {
        const prevTabLinkEl = $(".nav-tabs .active")
            .closest("li")
            .prev("li")
            .find("a")[0];
        const prevTab = new bootstrap.Tab(prevTabLinkEl);
        prevTab.show();
    });

    // --------------Access management drop down js --------------
    $(".dropdown-menu li label").click(function (event) {
        event.stopPropagation()
    })
    $(".role-drop-sec .dropend .dropdown-toggle").click(function (event) {
        event.stopPropagation();
        if ($(this).hasClass("show")) {
            $(".dropend .dropdown-toggle").removeClass("show");
            $(".dropend .dropdown-menu").removeClass("show");
            $(this).addClass("show");
            $(this).next(".dropdown-menu").addClass("show");
        }
        else {
            $(this).addClass("show");
            $(this).next(".dropdown-menu").addClass("show");
            $(this).next(".dropdown-menu").attr("data-popper-placement", "right-start");
            $(this).next(".dropdown-menu").css("transform", "translate(102px, -47px)");
        }
    })

    // --------------Sidebar Expanded js --------------
    $(".close-sidebar").click(function () {
        $('.sidebar-expanded').removeClass('sidebar-expanded')
    });

    $(".hamburger-toggle").click(function () {
        $(".sidebar-reduced").toggleClass("sidebar-expanded")
    });

    $(".menu-nav ul.menu-list li .menu-item-inner").click(function () {
        $(this).closest("li").toggleClass("is-active").siblings().removeClass('is-active');
    });

    // --------------Documents upload js js --------------
    // $(document).on('click', '#upload-img', function () {

    //     if ($('.wrapper-thumb img').attr('src') != '') {
    //         var selectoption = `<select class="selectpicker mb-2"><option selected="selected">File Type</option><option value="1">Documents</option><option value="2">Certificate</option><option value="3">DL</option><option value="4">Image</option></select>`;
    //         $("#img-preview").append(selectoption)
    //     }

    // });


    // $(document).on('click', '.remove-btn', function () {
    //     $(".bootstrap-select").remove()
    //     $(".selectpicker").remove()
    // });

     // --------------grid view and list view js js --------------
     $(".list-btn").click(function () {
        $(this).addClass("active");
        $(".grid-btn").removeClass("active");
        $(".data-table-sec").addClass("show-panel");
        $(".card-view-section").removeClass("show-panel");
    });
    $(".grid-btn").click(function () {
        $(this).addClass("active");
        $(".list-btn").removeClass("active");
        $(".data-table-sec").removeClass("show-panel");
        $(".card-view-section").addClass("show-panel");
    });

    // --------------grid view and list view js js --------------
    $(".damages-click").click(function () {
        if ($(this).is(":checked")) {
            $(".damages-show").slideDown("fast");
        } else {
            $(".damages-show").slideUp("fast");
        }
    });


});




// --------------Check your email js--------------
let digitValidate = function (ele) {
    console.log(ele.value);
    ele.value = ele.value.replace(/[^0-9]/g, '');
}

let tabChange = function (val) {
    let ele = document.querySelectorAll('.testinp');
    if (ele[val - 1].value != '') {
        ele[val].focus()
    } else if (ele[val - 1].value == '') {
        ele[val - 2].focus()
    }
}
// --------------dark theam and light theam js --------------
var html = document.getElementsByTagName('html');
var radios = document.getElementsByName('themes');

for (i = 0; i < radios.length; i++) {
    radios[i].addEventListener('change', function () {
        html[0].classList.remove(html[0].classList.item(0));
        html[0].classList.add(this.id);
    });
}
/* increase and decrease button js  */
var buttonPlus = $(".qty-btn-plus");
var buttonMinus = $(".qty-btn-minus");

var incrementPlus = buttonPlus.click(function () {
    var $n = $(this)
        .parent(".qty-container")
        .find(".input-qty");
    // $n.val(Number($n.val()) + 1);
    var amount = Number($n.val());
    $n.val(amount + 1);

});

var incrementMinus = buttonMinus.click(function () {
    var $n = $(this)
        .parent(".qty-container")
        .find(".input-qty");
    var amount = Number($n.val());
    if (amount > 1) {
        $n.val(amount - 1);
    }
});
/* End increase and decrease button js  */
// --------------tooltip  js--------------
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

// --------------avatar-upload js--------------
// Reusable function to handle file input and preview
function handleFileInput(inputId, previewId) {
    var input = document.getElementById(inputId);
    var preview = document.getElementById(previewId);

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            preview.style.backgroundImage = 'url(' + e.target.result + ')';
            preview.style.display = 'none';
            $(preview).fadeIn(650);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

// Event listeners for file inputs
$("#imageUpload").change(function () {
    handleFileInput("imageUpload", "imagePreview");
});

$("#imageUpload1").change(function () {
    handleFileInput("imageUpload1", "imagePreview1");
});

// --------------Documents upload js js --------------
function setupImageUpload(inputId, previewId, removeBtnClass) {
    var imgUpload = document.getElementById(inputId),
        imgPreview = document.getElementById(previewId),
        totalFiles, img;

    imgUpload.addEventListener('change', previewImgs, true);

    function previewImgs(event) {
        totalFiles = imgUpload.files.length;

        if (!!totalFiles) {
            imgPreview.classList.remove('img-thumbs-hidden');
        }

        for (var i = 0; i < totalFiles; i++) {
            var wrapper = document.createElement('div');
            wrapper.classList.add('wrapper-thumb');
            var removeBtn = document.createElement("span");
            var nodeRemove = document.createTextNode('x');
            removeBtn.classList.add(removeBtnClass);
            removeBtn.appendChild(nodeRemove);
            img = document.createElement('img');
            img.src = URL.createObjectURL(event.target.files[i]);
            img.classList.add('img-preview-thumb');
            wrapper.appendChild(img);
            wrapper.appendChild(removeBtn);
            imgPreview.appendChild(wrapper);

            // Add click event listener to remove the image
            $('.' + removeBtnClass).click(function () {
                $(this).parent('.wrapper-thumb').remove();
            });
        }
    }
}

// Call the setupImageUpload function for the first image upload
setupImageUpload('upload-img', 'img-preview', 'remove-btn');

// Call the setupImageUpload function for the second image upload
setupImageUpload('upload-img1', 'img-preview1', 'remove-btn');


// -----------------------active inactive button performing checkbox in manage team-------------------
// Get a reference to the checkbox element
var checkbox = document.querySelector('input[type="checkbox"]');

// Add a click event listener to the .slider element
document.querySelector('.slider').addEventListener('click', function(event) {
  // Toggle the checkbox state (check if unchecked, uncheck if checked)
  checkbox.checked = !checkbox.checked;
});


ClassicEditor
    .create(document.querySelector('.editor3'))
    .catch(error => {
        return error
    });
ClassicEditor
    .create(document.querySelector('.editor4'))
    .catch(error => {
        return error
    });

ClassicEditor
    .create(document.querySelector('.editor5'))
    .catch(error => {
        return error
    });
ClassicEditor
    .create(document.querySelector('.editor6'))
    .catch(error => {
        return error
    });

ClassicEditor
    .create(document.querySelector('.editor8'))
    .catch(error => {
        return error
    });
ClassicEditor
    .create(document.querySelector('.editor9'))
    .catch(error => {
        return error
    });

ClassicEditor
    .create(document.querySelector('.editor10'))
    .catch(error => {
        return error
    });

ClassicEditor
    .create(document.querySelector('.editor11'))
    .catch(error => {
        return error
    });
ClassicEditor
    .create(document.querySelector('.editor12'))
    .catch(error => {
        return error
    });




//I added event handler for the file upload control to access the files properties.
document.addEventListener("DOMContentLoaded", init, false);

//To save an array of attachments
var AttachmentArray = [];

//counter for attachment array
var arrCounter = 0;

//to make sure the error message for number of files will be shown only one time.
var filesCounterAlertStatus = false;

//un ordered list to keep attachments thumbnails
var ul = document.createElement("ul");
ul.className = "thumb-Images";
ul.id = "imgList";

function init() {
    //add javascript handlers for the file upload event
    document
        .querySelector("#files")
        .addEventListener("change", handleFileSelect, false);
}

//the handler for file upload event
function handleFileSelect(e) {
    //to make sure the user select file/files
    if (!e.target.files) return;

    //To obtaine a File reference
    var files = e.target.files;

    // Loop through the FileList and then to render image files as thumbnails.
    for (var i = 0, f; (f = files[i]); i++) {
        //instantiate a FileReader object to read its contents into memory
        var fileReader = new FileReader();

        // Closure to capture the file information and apply validation.
        fileReader.onload = (function (readerEvt) {
            return function (e) {
                //Apply the validation rules for attachments upload
                ApplyFileValidationRules(readerEvt);

                //Render attachments thumbnails.
                RenderThumbnail(e, readerEvt);

                //Fill the array of attachment
                FillAttachmentArray(e, readerEvt);
            };
        })(f);

        // Read in the image file as a data URL.
        // readAsDataURL: The result property will contain the file/blob's data encoded as a data URL.
        // More info about Data URI scheme https://en.wikipedia.org/wiki/Data_URI_scheme
        fileReader.readAsDataURL(f);
    }
    document
        .getElementById("files")
        .addEventListener("change", handleFileSelect, false);
}

//To remove attachment once user click on x button
jQuery(function ($) {
    $("div").on("click", ".img-wrap .close", function () {
        var id = $(this)
            .closest(".img-wrap")
            .find("img")
            .data("id");

        //to remove the deleted item from array
        var elementPos = AttachmentArray.map(function (x) {
            return x.FileName;
        }).indexOf(id);
        if (elementPos !== -1) {
            AttachmentArray.splice(elementPos, 1);
        }

        //to remove image tag
        $(this)
            .parent()
            .find("img")
            .not()
            .remove();

        //to remove div tag that contain the image
        $(this)
            .parent()
            .find("div")
            .not()
            .remove();

        //to remove div tag that contain caption name
        $(this)
            .parent()
            .parent()
            .find("div")
            .not()
            .remove();

        //to remove li tag
        var lis = document.querySelectorAll("#imgList li");
        for (var i = 0; (li = lis[i]); i++) {
            if (li.innerHTML == "") {
                li.parentNode.removeChild(li);
            }
        }
    });
});

//Apply the validation rules for attachments upload
function ApplyFileValidationRules(readerEvt) {
    //To check file type according to upload conditions
    if (CheckFileType(readerEvt.type) == false) {
        alert(
            "The file (" +
            readerEvt.name +
            ") does not match the upload conditions, You can only upload jpg/png/gif files"
        );
        e.preventDefault();
        return;
    }

    //To check file Size according to upload conditions
    if (CheckFileSize(readerEvt.size) == false) {
        alert(
            "The file (" +
            readerEvt.name +
            ") does not match the upload conditions, The maximum file size for uploads should not exceed 300 KB"
        );
        e.preventDefault();
        return;
    }

    //To check files count according to upload conditions
    if (CheckFilesCount(AttachmentArray) == false) {
        if (!filesCounterAlertStatus) {
            filesCounterAlertStatus = true;
            alert(
                "You have added more than 10 files. According to upload conditions you can upload 10 files maximum"
            );
        }
        e.preventDefault();
        return;
    }
}

//To check file type according to upload conditions
function CheckFileType(fileType) {
    if (fileType == "image/jpeg") {
        return true;
    } else if (fileType == "image/png") {
        return true;
    } else if (fileType == "image/gif") {
        return true;
    } else {
        return false;
    }
    return true;
}

//To check file Size according to upload conditions
function CheckFileSize(fileSize) {
    if (fileSize < 300000) {
        return true;
    } else {
        return false;
    }
    return true;
}

//To check files count according to upload conditions
function CheckFilesCount(AttachmentArray) {
    //Since AttachmentArray.length return the next available index in the array,
    //I have used the loop to get the real length
    var len = 0;
    for (var i = 0; i < AttachmentArray.length; i++) {
        if (AttachmentArray[i] !== undefined) {
            len++;
        }
    }
    //To check the length does not exceed 10 files maximum
    if (len > 9) {
        return false;
    } else {
        return true;
    }
}

//Render attachments thumbnails.
function RenderThumbnail(e, readerEvt) {
    var li = document.createElement("li");
    ul.appendChild(li);
    li.innerHTML = [
        '<div class="img-wrap"> <span class="close">&times;</span>' +
        '<img class="thumb" src="',
        e.target.result,
        '" title="',
        escape(readerEvt.name),
        '" data-id="',
        readerEvt.name,
        '"/>' + "</div>"
    ].join("");

    var div = document.createElement("div");
    div.className = "FileNameCaptionStyle";
    li.appendChild(div);
    div.innerHTML = [readerEvt.name].join("");
    document.getElementById("Filelist").insertBefore(ul, null);
}

//Fill the array of attachment
function FillAttachmentArray(e, readerEvt) {
    AttachmentArray[arrCounter] = {
        AttachmentType: 1,
        ObjectType: 1,
        FileName: readerEvt.name,
        FileDescription: "Attachment",
        NoteText: "",
        MimeType: readerEvt.type,
        Content: e.target.result.split("base64,")[1],
        FileSizeInBytes: readerEvt.size
    };
    arrCounter = arrCounter + 1;
}

// --------------chat window pop  js--------------
// var running = false;
// function send() {
//     if (running == true) return;
//     var msg = document.getElementById("message").value;
//     if (msg == "") return;
//     running = true;
//     addMsg(msg);
//     window.setTimeout(addResponseMsg, 1000, msg);
// }
// function addMsg(msg) {
//     var div = document.createElement("div");
//     div.innerHTML =
//         "<span style='flex-grow:1'></span><div class='chat-message-sent'>" +
//         msg +
//         "</div>";
//     div.className = "chat-message-div";
//     document.getElementById("message-box").appendChild(div);
//     document.getElementById("message").value = "";
//     document.getElementById("message-box").scrollTop = document.getElementById(
//         "message-box"
//     ).scrollHeight;
// }
// function addResponseMsg(msg) {
//     var div = document.createElement("div");
//     div.innerHTML = "<div class='chat-message-received'>" + msg + "</div>";
//     div.className = "chat-message-div";
//     document.getElementById("message-box").appendChild(div);
//     document.getElementById("message-box").scrollTop = document.getElementById(
//         "message-box"
//     ).scrollHeight;
//     running = false;
// }

// document.getElementById("chatbot_toggle").onclick = function () {
//     if (document.getElementById("chatbot").classList.contains("collapsed")) {
//         document.getElementById("chatbot").classList.remove("collapsed")
//         document.getElementById("chatbot_toggle").children[0].style.display = "none"
//         document.getElementById("chatbot_toggle").children[1].style.display = ""
//         setTimeout(addResponseMsg, 1000, "Hi")
//     }
//     else {
//         document.getElementById("chatbot").classList.add("collapsed")
//         document.getElementById("chatbot_toggle").children[0].style.display = ""
//         document.getElementById("chatbot_toggle").children[1].style.display = "none"
//     }
// }




