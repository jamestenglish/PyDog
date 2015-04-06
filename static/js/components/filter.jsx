var Filter = React.createClass({
    handleChange: function () {
        var node = React.findDOMNode(this.refs.filter);

        DogActions.filter(node.value.trim());
    },
    render: function () {

        return (
            <form className="navbar-form navbar-left" role="search">
                <div className="form-group">
                    <input ref="filter" type="text" className="form-control" placeholder="Filter" onChange={this.handleChange} />
                </div>
            </form>
            );
    }
});