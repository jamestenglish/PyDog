var Filter = React.createClass({
    componentDidMount: function() {
        var node = React.findDOMNode(this.refs.filter);
        node.value = reactCookie.load('filter') || '';
    },
    handleChange: function () {
        var node = React.findDOMNode(this.refs.filter);

        DogActions.filter(node.value.trim());
    },
    render: function () {

        return (
            <form className="navbar-form navbar-left" role="search">
                <div className="form-group">
                    <input ref="filter" type="text" className="form-control" placeholder="Breeds to Exclude" onChange={this.handleChange} />
                </div>
            </form>
            );
    }
});