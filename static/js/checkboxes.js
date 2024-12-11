document.getElementById('editableCheckbox').addEventListener('change', function() {
    var messageElement = document.getElementById('message');
    if (this.checked) {
        messageElement.style.display = 'block';
    } else {
        messageElement.style.display = 'none';
    }
});

