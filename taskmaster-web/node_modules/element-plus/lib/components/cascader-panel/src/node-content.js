'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

var vue = require('vue');
var index = require('../../../hooks/use-namespace/index.js');
var shared = require('@vue/shared');

function isVNodeEmpty(vnodes) {
  return !!(shared.isArray(vnodes) ? vnodes.every(({
    type
  }) => type === vue.Comment) : (vnodes == null ? void 0 : vnodes.type) === vue.Comment);
}
var NodeContent = vue.defineComponent({
  name: "NodeContent",
  props: {
    node: {
      type: Object,
      required: true
    },
    renderLabelFn: Function
  },
  setup(props) {
    const ns = index.useNamespace("cascader-node");
    const {
      renderLabelFn,
      node
    } = props;
    const {
      data,
      label: nodeLabel
    } = node;
    const label = () => {
      const renderLabel = renderLabelFn == null ? void 0 : renderLabelFn({
        node,
        data
      });
      return isVNodeEmpty(renderLabel) ? nodeLabel : renderLabel != null ? renderLabel : nodeLabel;
    };
    return () => vue.createVNode("span", {
      "class": ns.e("label")
    }, [label()]);
  }
});

exports["default"] = NodeContent;
//# sourceMappingURL=node-content.js.map
