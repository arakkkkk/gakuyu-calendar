function set_alert(icon, text, color) {
  if (icon == "check") {
    icon = `<svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" fill="currentColor" class="bi bi-check-lg mr-4" viewBox="0 0 16 16">
					    <path d="M13.485 1.431a1.473 1.473 0 0 1 2.104 2.062l-7.84 9.801a1.473 1.473 0 0 1-2.12.04L.431 8.138a1.473 1.473 0 0 1 2.084-2.083l4.111 4.112 6.82-8.69a.486.486 0 0 1 .04-.045z"/>
				    </svg>`;
  } else if (icon == "alert") {
    icon = `<svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" fill="currentColor" class="bi bi-exclamation-triangle" viewBox="0 0 16 16">
              <path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.146.146 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.163.163 0 0 1-.054.06.116.116 0 0 1-.066.017H1.146a.115.115 0 0 1-.066-.017.163.163 0 0 1-.054-.06.176.176 0 0 1 .002-.183L7.884 2.073a.147.147 0 0 1 .054-.057zm1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566z"/>
              <path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995z"/>
            </svg>`
  }
 
  var alert_html =
    `
		<div class="alert alert-` +
    color +
    ` alert-dismissible fade show alert-overlay" role="alert">
			` +
    icon +
    text +
    `
			<button type="button" class="close" data-dismiss="alert" aria-label="Close">
			<span aria-hidden="true">&times;</span>
			</button>
		</div>
			`;
  document.getElementById("alert_area").innerHTML = alert_html;
  window.setTimeout(function () {
    $(".alert").alert("close");
  }, 3000);
}

// dateのinput formを当日の日付に初期化する
const initDateForm = () => {
  let today = new Date();
  today.setDate(today.getDate());
  let yyyy = today.getFullYear();
  let mm = ("0" + (today.getMonth() + 1)).slice(-2);
  let dd = ("0" + today.getDate()).slice(-2);
  let today_value = yyyy + '-' + mm + '-' + dd;

  let $date_forms = document.querySelectorAll("input[type=date]")
  for(let $date_form of $date_forms) {
    $date_form.value = today_value
  }
}

// table要素を指定したカラムで絞りこむためのselectboxを作る関数
const set_filterselections = (filter_nums, $table=document.querySelector("table")) => {
  let $selection = document.querySelector("filterSelections")
  $selection.innerHTML = ""
  let contents = ""
  
  for(let filter_num of filter_nums) {
    let header_label =$table.querySelectorAll("th")[filter_num].innerText
    contents += `<a>${header_label}</a>
                <select id="filter_${String(filter_num)}" onchange="">
                  <option value="">-</option>`
    let check_list = []
    for(let $tr of $table.querySelector("tbody").querySelectorAll("tr")) {
      let selection_label = $tr.querySelectorAll("td")[filter_num].innerText
      if(check_list.includes(selection_label)) {
        continue
      } else {
        contents += `<option value="${selection_label}">${selection_label}</option>`
        check_list.push(selection_label)
      }
    }
    contents += "</select></br>"
  }
  $selection.innerHTML = contents
}

// 上で作成したselectboxで絞り混みを実行する関数
const submit_filter = ($table=document.querySelector("table")) => {
  for($tr of $table.querySelector("tbody").querySelectorAll("tr")) {
    $tr.hidden = false
  }

  $selection_parent = document.querySelector("filterSelections")
  for(let $selection of $selection_parent.querySelectorAll("select")) {
    if($selection.value == "") continue
    let selection_num = Number($selection.getAttribute("id").split("_")[1])
    for($tr of $table.querySelector("tbody").querySelectorAll("tr")) {
      if($tr.querySelectorAll("td")[selection_num].innerText != $selection.value) {
        $tr.hidden = true
      }
    }
  }
}
