function deletePost(btn) {

    let post_id = btn.dataset.id
    $.ajax({
        url: "/ajax/deletePost",
        type: "POST",
        data: { id: post_id },
        success: function () {
            let elements = document.querySelectorAll('.IndexPosts');
            for (let i = 0; i < elements.length; i++) {
                if (elements[i].id == post_id) {
                    elements[i].style.display = 'none';
                    break;
                };
            };
        }
    });
};
