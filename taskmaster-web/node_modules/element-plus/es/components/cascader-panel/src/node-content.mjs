import { defineComponent, createVNode, Comment } from 'vue';
import { useNamespace } from '../../../hooks/use-namespace/index.mjs';
import { isArray } from '@vue/shared';

function isVNodeEmpty(vnodes) {
  return !!(isArray(vnodes) ? vnodes.every(({
    type
  }) => type === Comment) : (vnodes == null ? void 0 : vnodes.type) === Comment);
}
var NodeContent = defineComponent({
  name: "NodeContent",
  props: {
    node: {
      type: Object,
      required: true
    },
    renderLabelFn: Function
  },
  setup(props) {
    const ns = useNamespace("cascader-node");
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
    return () => createVNode("span", {
      "class": ns.e("label")
    }, [label()]);
  }
});

export { NodeContent as default };
//# sourceMappingURL=node-content.mjs.map
