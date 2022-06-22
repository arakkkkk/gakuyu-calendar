const edit_handler = ($target) => {
  $target.querySelector("#edit").hidden = true
  $target.querySelector("a").hidden = true
  $target.querySelector("#cancel").hidden = false
  $target.querySelector("#submit").hidden = false
  $target.querySelector("input").hidden = false
}
const cancel_handler = ($target, event_id) => {
  $target.querySelector("#edit").hidden = false
  $target.querySelector("a").hidden = false
  $target.querySelector("#cancel").hidden = true
  $target.querySelector("#submit").hidden = true
  $target.querySelector("input").hidden = true
}
const submit_handler = ($target, event_id) => {
  $target.querySelector("#edit").hidden = false
  $target.querySelector("a").hidden = false
  $target.querySelector("#cancel").hidden = true
  $target.querySelector("#submit").hidden = true
  $target.querySelector("input").hidden = true
  $input = $target.querySelector("input")
  let json = {event_id: event_id}
  json[$input.getAttribute("id")] = $input.value

  $.ajax({
    type: "POST",
    url: "/api/equipments/update",
    contentType: "application/json",
    data: JSON.stringify(json),
    dataType: "json",
    scriptCharset: "utf-8",
    beforeSend: function () {
      $("#overlay").fadeIn();
    }
  })
  .done(function (result) {
    set_alert("check", "変更されました。", "success")
    $target.querySelector("a").innerHTML = $input.value
  })
  .fail(function (data, jqXHR, textStatus, errorThrown) {
    set_alert("alert", "ネットワークを確認してください。", "danger")
  })
  .always(function () {
    $("#overlay").fadeOut();
  });
}

const inputBoxComponent = (content, event_id, key) => {
  if(content == undefined) content = ""
  return `
  <input id="${key}" hidden />
  <button id="submit" onclick="submit_handler(this.parentElement, ${event_id})" hidden>確定</button>
  <button id="cancel" onclick="cancel_handler(this.parentElement)" hidden>取消</button>
  <a>${content}</a>
  <button id="edit" onclick="edit_handler(this.parentElement)">変更</button>`
} 
