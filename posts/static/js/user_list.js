function goToDetail(user) {
  $.ajax({
    type: 'GET',
    url: "/user/detail",
    data: {
      'user_id': user
    },
    success: function (response) {
      const data = JSON.parse(response);
      const type = data?.fields?.type === 'a' ? 'Admin' : 'User';

      console.log('user', data);
      filename = ''
      if (data?.profile) {
        lastFileName = data.profile.split('/');
        filename = lastFileName[lastFileName.length - 1];
      } else {
        filename = 'user-default.png';
      }
      filename ? $("#user-detail-profile").attr("src", '/media/' + filename) : '';
      data?.fields?.name ? $("#user-detail-name").html(data.fields.name) : '';
      $("#type").html(type);
      data?.fields?.email ? $("#user-detail-email").html(data.fields.email) : '';
      data?.fields?.phone ? $("#phone").html(data.fields.phone) : '';
      data?.fields?.created_at ? $("#created_date").html(data.fields.created_at) : '';
      data?.fields?.created_user_name ? $("#created_user").html(data.created_user_name) : '';
      data?.fields?.updated_at ? $("#updated_date").html(data.fields.updated_at) : '';
      data?.updated_user_name ? $("#updated_user").html(data.updated_user_name) : '';
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}

function showUserDeleteDialog(user) {
  $.ajax({
    type: 'GET',
    url: "/user/detail/",
    data: {
      'user_id': user
    },
    success: function (response) {
      const data = JSON.parse(response);
      let type = data.fields.type === "a" ? 'Admin' : 'User';
      $("#user-delete-id").html(user);
      $("#user-delete-name").html(data.fields.name);
      $("#user-delete-type").html(type);
      $("#user-delete-email").html(data.fields.email);
      $("#user-delete-phone").html(data.fields.phone);
      $("#user-delete-dob").html(data.fields.dob);
      $("#user-delete-address").html(data.fields.address);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}

function userDelete() {
  const id = $("#user-delete-id").html();
  $.ajax({
    type: 'GET',
    url: "/user/delete",
    data: {
      'user_id': id
    },
    success: function () {
      $("#deleteUserModal").modal('hide');
      location.reload(true);
    },
    error: function (response) {
      alert(response["responseJSON"]["error"]);
    }
  })
}