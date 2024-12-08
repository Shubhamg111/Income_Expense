const searchField = document.querySelector('#searchField')
const tableOutput = document.querySelector('.table-output')
const appTable = document.querySelector('.app-table')
const paginationContainer = document.querySelector('.pagination-container')
const tBody = document.querySelector('.table-body')






tableOutput.style.display = "none"
searchField.addEventListener('keyup',(e)=>{

    const searchValue = e.target.value

    if(searchValue.trim().length > 0){
        tBody.innerHTML=""
        fetch('/search-expenses',{

            body: JSON.stringify({searchText:searchValue}),
            method: 'POST',
            })
            .then((res)=> res.json())
            .then((data)=> {
                paginationContainer.style.display= "none"
                console.log("data",data)
                appTable.style.display="none"
                tableOutput.style.display = "block"

                if (data.length === 0){
                    tableOutput.innerHTML= 'No Result '
                }
                else{
                    data.forEach(item => {
                        tBody.innerHTML +=
                        `
                        <tr>

                        <td>${item.amount}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        <td><a href="{% url 'expense-edit' item.id %}" class="btn btn-secondary">Edit</a></td>
                            
                        </tr>


                        `
                    });

                }
                
            })
    }
    else{
        tableOutput.style.display = "none"

        appTable.style.display="block"
        paginationContainer.style.display= "block"

    }

})