var libraries = [];
$.ajax({
    url: '../allcourses/',
    type: 'GET',
    success: function(response) {
      console.log("hahaha")
      document.getElementById("")
      var names = response.split("{u\'course_name\': u\'")
      var ids = response.split("u\'course_id\': ")
      if(names.length <= 1)
      {
        libraries.push({course_id: "0", course_name: "No Courses"});
      }
        for(var i = 1; i<names.length;i++)
        {
          cname = names[i].split("\', u\'prereq")[0]
          cid = ids[i].split("L")[0]
          libraries.push({course_id: cid, course_name: cname});

        }
        console.log(libraries)
        console.log("logged in");
        React.renderComponent(
    		    <SearchExample items={libraries} />,
    		    document.body
    		);
    },
    error: function(error) {
        console.log(error);
    },

});

console.log("yo");
console.log(libraries);