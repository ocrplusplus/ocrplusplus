var Profilename = React.createClass({
	getInitialState: function() {
		return null;
	},
	render : function() {
		var name = this.props.user;
		return <span> {name} </span>;
	}
});

ReactDOM.render(
	<Profilename user="shubham"/>,
	document.getElementById('namediv')
	);
