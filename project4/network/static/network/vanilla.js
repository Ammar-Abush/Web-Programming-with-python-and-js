document.addEventListener('DOMContentLoaded', function () {
  console.log("WHY ARE WE HERE");
  const likeButtons = document.querySelectorAll('.like-button');

  likeButtons.forEach((button) => {
      button.addEventListener('click', function () {
          const postId = this.dataset.id;
          var post = button.closest(".post");
          console.log(post)
          fetch(`/like_post/${postId}/`, {
              method: 'POST',
              headers: {
                  'X-CSRFToken': getCookie('csrftoken'),
              }
          })
          .then(response => response.json())
          .then(result => {
              const r = result;
              console.log(r['liked']);
              if (r['liked']) {
                  const heartIcon = this.querySelector('i.bi-heart');
                  heartIcon.classList.remove('bi-heart');
                  heartIcon.classList.add('bi-heart-fill');
                  var c = post.querySelector(".counter").innerHTML
                  c = parseInt(c); 
                  post.querySelector(".counter").innerHTML = c + 1;
    
              } else {
                  const heartIcon = this.querySelector('i.bi-heart-fill');
                  heartIcon.classList.remove('bi-heart-fill');
                  heartIcon.classList.add('bi-heart');
                  var c = post.querySelector(".counter").innerHTML
                  c = parseInt(c); 
                  post.querySelector(".counter").innerHTML = c - 1;
                 

              }
              console.log(r);
          })
          .catch(error => {
              console.error('Error:', error);
          });
      });
  });
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}
