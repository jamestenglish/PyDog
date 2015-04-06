var Job = React.createClass({
    handleClick: function () {
        JobActions.post();
    },
    render: function () {
        var error = (<span />);
        if (this.props.data.hasOwnProperty('error')) {
            error = (<span className="text-danger">{this.props.data['error']}</span>);
        }

        var status = (<span />);
        if (this.props.data.hasOwnProperty('job_id') && this.props.data.hasOwnProperty('done') && !this.props.data.done) {
            status = (<span className="text-success">Working...</span>);
        }
        return (
            <div className="job">
                <button className="btn btn-success navbar-btn" onClick={this.handleClick}>Reload List</button>
                {error}
                {status}
            </div>
            );
    }
});