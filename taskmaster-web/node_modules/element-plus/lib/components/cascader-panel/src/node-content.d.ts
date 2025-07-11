import type { PropType } from 'vue';
import type { CascaderNode, RenderLabel } from './types';
declare const _default: import("vue").DefineComponent<{
    node: {
        type: PropType<CascaderNode>;
        required: true;
    };
    renderLabelFn: PropType<RenderLabel>;
}, () => JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, Record<string, any>, string, import("vue").VNodeProps & import("vue").AllowedComponentProps & import("vue").ComponentCustomProps, Readonly<import("vue").ExtractPropTypes<{
    node: {
        type: PropType<CascaderNode>;
        required: true;
    };
    renderLabelFn: PropType<RenderLabel>;
}>>, {}>;
export default _default;
