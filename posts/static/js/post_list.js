function goToDetail(post) {
  $.ajax({
    type: 'GET',
    url: "/post/detail",
    data: {
      'post_id': post
    },
    success: function (response) {
      const data = JSON.parse(response);
      let status = data.fields.status === 1 ? 'Active' : 'Not Active';
      $("#title").html(data.fields.title);
      $("#description").html(data.fields.description);
      $("#status").html(status);
      $("#created_date").html(data.fields.created_at);
      $("#created_user").html(data.created_user_name);
      $("#updated_date").html(data.fields.updated_at);
      $("#updated_user").html(data.updated_user_name);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}

function downloadCSV(postList) {
  $.ajax({
    type: 'GET',
    url: "/post/list/download",
    data: {},
    success: function (response) {
      let hiddenElement = document.createElement('a');
      const today = new Date();
      const date = today.getFullYear().toString() + (today.getMonth() + 1).toString() + today.getDate().toString() +
        today.getHours().toString() + today.getMinutes().toString() + today.getSeconds().toString();
      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(response);
      hiddenElement.target = '_blank';
      hiddenElement.download = 'post_list' + date + '_' + '.csv';
      hiddenElement.click();
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })

}

function showPostDeleteDialog(post) {
  $.ajax({
    type: 'GET',
    url: "/post/detail/",
    data: {
      'post_id': post
    },
    success: function (response) {
      const data = JSON.parse(response);
      let status = data.fields.status === "1" ? 'Active' : 'Not Active';
      $("#post-delete-id").html(post);
      $("#post-delete-title").html(data.fields.title);
      $("#post-delete-description").html(data.fields.description);
      $("#post-delete-status").html(status);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}

function postDelete() {
  const id = $("#post-delete-id").html();
  $.ajax({
    type: 'GET',
    url: "/post/delete",
    data: {
      'post_id': id
    },
    success: function () {
      $("#deletePostModal").modal('hide');
      location.reload(true);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}