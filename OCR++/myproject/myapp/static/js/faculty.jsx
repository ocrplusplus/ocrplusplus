import AppBar from 'material-ui/lib/app-bar'

ReactDOM.render(<AppBar />, document.getElementById("container"));

// FormlyConfig.fields.addType([
//   { name: 'text', field: require('./components/field-types/TextField') },
//   { name: 'number', field: require('./components/field-types/NumberField') },
//   { name: 'checkbox', field: require('./components/field-types/Checkbox') }
// ]);
//
// var App = React.createClass({
//   getInitialState: function() {
//     return { model: {} };
//   },
//   onFormlyUpdate: function(model) {
//     this.setState({model: model});
//   },
//   componentWillMount: function() {
//     this.formlyConfig = {
//       name: 'myFormly',
//       fields: [
//         {
//           key: 'name',
//           type: 'text',
//           label: 'Name',
//           placeholder: 'If you would be so kind...',
//           hidden: function(model) {
//             return !!model.secretName;
//           }
//         },
//         {
//           key: 'age',
//           type: 'number',
//           label: 'Age'
//         },
//         {
//           key: 'secretName',
//           type: 'text',
//           label: 'Secret name...?',
//           placeholder: 'If you have no name...',
//           hidden: function(model) {
//             return !!model.name;
//           }
//         },
//         {
//           key: 'awesome',
//           type: 'checkbox',
//           label: 'Are you awesome?'
//         }
//       ]
//     };
//   },
//   render: function() {
//     return (
//       <div className="container">
//         <h2>Form</h2>
//         <Formly config={this.formlyConfig} model={this.state.model} onFormlyUpdate={this.onFormlyUpdate} />
//
//         <h2>Model:</h2>
//         <pre>{JSON.stringify(this.state.model, null, 2)}</pre>
//       </div>
//     );
//   }
// });
//
// ReactDOM.render(React.createElement(App, null), document.body);
