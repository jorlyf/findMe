let count = 1;
let role;


function createPost(post) {
    let id = post['id'];

    let indexPost = document.createElement("div");

    indexPost.className = 'IndexPosts';
    indexPost.id = id;
    document.getElementById('posts').appendChild(indexPost);

    let indexDateHead = document.createElement("div");
    indexDateHead.id = id + 'IndexDateHead';
    indexDateHead.className = 'IndexDateHead';
    document.getElementById(id).appendChild(indexDateHead);

    let date = document.createElement("p");
    date.className = 'Date';
    date.textContent = post['date'];
    document.getElementById(id + 'IndexDateHead').appendChild(date);

    let head_name = document.createElement("h2");
    head_name.className = 'Head_name';
    head_name.textContent = post['head_name'];
    document.getElementById(id + 'IndexDateHead').appendChild(head_name);

    let description = document.createElement("p");
    description.className = 'Description';
    description.textContent = post['description'];
    document.getElementById(id).appendChild(description);

    if (post['images']) {
        let images = document.createElement("img");
        images.className = 'indexImage';
        images.setAttribute('src', '/static/images/posts/' + post['images']);
        document.getElementById(id).appendChild(images);
    }

    let contactsBox = document.createElement("div");
    contactsBox.id = id+'Contacts';
    contactsBox.className = 'iconContainer';
    document.getElementById(id).appendChild(contactsBox);

    if (post['vk']) {
        let vk = document.createElement("div");
        vk.id = id+'Vk';
        vk.className = 'contacts';
        let image = document.createElement("img");
        let text = document.createElement("p");
        image.setAttribute('src', 'static/images/vkIcon.png');
        image.setAttribute('width', '32');
        image.setAttribute('height', '32');
        text.textContent = post['vk'];
        document.getElementById(id+'Contacts').appendChild(vk);
        document.getElementById(id+'Vk').appendChild(image);
        document.getElementById(id+'Vk').appendChild(text);
    }

    if (post['instagram']) {
        let instagram = document.createElement("div");
        instagram.id = id+'Instagram';
        instagram.className = 'contacts';
        let image = document.createElement("img");
        let text = document.createElement("p");
        image.setAttribute('src', 'static/images/instagramIcon.png');
        image.setAttribute('width', '32');
        image.setAttribute('height', '32');
        text.textContent = post['instagram'];
        document.getElementById(id+'Contacts').appendChild(instagram);
        document.getElementById(id+'Instagram').appendChild(image);
        document.getElementById(id+'Instagram').appendChild(text);
    }

    if (post['otherContacts']) {
        let otherContacts = document.createElement("div");
        otherContacts.id = id+'OtherContacts';
        otherContacts.className = 'contacts';
        let image = document.createElement("img");
        let text = document.createElement("p");
        image.setAttribute('src', 'static/images/otherIcon.png');
        image.setAttribute('width', '32');
        image.setAttribute('height', '32');
        text.textContent = post['otherContacts'];
        document.getElementById(id+'Contacts').appendChild(otherContacts);
        document.getElementById(id+'OtherContacts').appendChild(image);
        document.getElementById(id+'OtherContacts').appendChild(text);
    }

    if (role == 'admin') {
        let btn = document.createElement("button");
        btn.id = 'deletePostBtn';
        btn.className = 'btn btn-outline-light me-2';
        btn.textContent = 'Удалить';
        btn.setAttribute('data-id', id);
        btn.setAttribute('onclick', 'deletePost(this)');
        document.getElementById(id).appendChild(btn);
    }
}


function show() {

    $.ajax({
        url: "/ajax/showPosts",
        type: "GET",
        data: { count: count },
        dataType: 'json',
    }).done(function (data) {
        role = data[1]['role'];

        for (post of data[0]) {
            createPost(post);
        }
        count++
    });
};


document.addEventListener('DOMContentLoaded', function() {
    show()
});

window.addEventListener('scroll', function() {
    if ( (document.documentElement.clientHeight + window.pageYOffset) >= (document.documentElement.scrollHeight ) )
        show();
});
