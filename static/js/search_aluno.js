function search_aluno() {
    // Declare variables
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('input-pesquisa');
    filter = input.value.toUpperCase();
    ul = document.getElementById("aluno-pesquisa");
    li = ul.getElementsByTagName('li');
  
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
      a = li[i].getElementsByTagName("a")[0];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }

  function search_aluno_table() {
    // Declare variables
    var input, filter, tbody, tr, a, i, txtValue;
    input = document.getElementById('input-pesquisa');
    filter = input.value.toUpperCase();
    tbody = document.getElementById("aluno-pesquisa_table");
    tr = tbody.getElementsByTagName('tr');
  
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      a = tr[i].getElementsByTagName("a")[0];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }