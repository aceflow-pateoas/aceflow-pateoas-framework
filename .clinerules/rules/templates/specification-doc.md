# Git 提交信息规范 (v1.1)

本规范旨在使Git提交历史清晰、可追溯，并为自动化工具（如生成CHANGELOG）提供支持。所有提交都必须遵循 Conventional Commits 标准。

## 1. 提交格式

完整的提交信息格式如下：
```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

## 2. 核心元素

### Header (必需)
- **type (必需):** 描述提交的类型，必须是以下之一：
  - `feat`: 新增功能
  - `fix`: 修复bug
  - `docs`: 仅文档变更
  - `style`: 代码格式变更（不影响代码逻辑）
  - `refactor`: 代码重构（既不是新增功能，也不是修复bug）
  - `perf`: 性能优化
  - `test`: 新增或修改测试
  - `build`: 影响构建系统或外部依赖的更改
  - `ci`: CI配置文件和脚本的更改
  - `chore`: 其他不修改代码或测试的杂项变动

- **scope (可选):** 影响范围（例如: `auth`, `user-api`, `cart-ui`）。

- **subject (必需):** 简短描述，动词开头，首字母小写，不超过50个字符。

### Body (可选)
对提交的详细描述，解释变更的原因和具体内容。

### Footer (可选)
用于标记**不兼容变更**或**关闭Issue**。
- **不兼容变更:** 必须以 `BREAKING CHANGE:` 开头。
- **关闭Issue:** 例如 `Closes #123, #456`。

## 3. 示例

**简单的修复:**
```
fix(user-api): prevent null pointer exception on missing profile
```

**新增功能 (带详细描述):**
```
feat(cart-ui): add item quantity controls in shopping cart

- Users can now increment, decrement, or manually enter the quantity
  for each item directly in the cart view.
- Input is debounced to avoid excessive API calls.

Closes #238
```

**重构 (带不兼容变更):**
```
refactor(auth): replace JWT library with Opaque Tokens

BREAKING CHANGE: The /auth/token endpoint no longer returns a JWT.
Clients must now treat the token as an opaque string and use the
/auth/introspect endpoint for validation.
```
```

---

### **Java 后端编码规范 (`java-coding-spec.md`)**

```markdown
# Java 后端编码规范 (v1.2)

本规范基于《阿里巴巴Java开发手册》，并针对我们团队的技术栈进行补充和强调。

## 1. 核心原则
- **格式统一:** 所有代码格式由项目根目录的 `.editorconfig` 和 `checkstyle.xml` 文件定义并强制执行。
- **清晰健壮:** 代码应易于理解，并能妥善处理异常情况。
- **避免魔法值:** 禁止在代码中直接使用未定义的字符串或数字，应定义为常量。

## 2. 最佳实践

### Optional 使用
- **推荐:** 仅用作方法的返回类型，表示一个可能为空的结果。
- **禁止:** 禁止用作方法参数或类字段。
- **处理:** 优先使用 `.orElseThrow()`, `.ifPresent()`, `.map()`，避免直接调用 `.get()`。

### Stream API
- **可读性:** 超过3个链式操作的复杂Stream，应考虑换行或提取到独立方法中。
- **性能:** 谨慎使用并行流 (`.parallelStream()`)，仅在CPU密集型且数据量大的无状态操作中考虑。

### 异常处理
- **自定义异常:** 业务异常必须是继承自 `RuntimeException` 的具体异常（e.g., `OrderNotFoundException`）。
- **事务:** 确保 `@Transactional` 注解的方法能正确回滚（默认对`RuntimeException`生效）。
- **日志:** `catch` 块中必须记录日志，并根据情况重新抛出或包装为自定义异常。

### 日志记录 (SLF4J)
- **级别:** `INFO` (关键流程), `WARN` (可恢复问题), `ERROR` (需要人工介入)。
- **格式:** 使用 `{}` 占位符，而不是字符串拼接。例如: `log.info("Processing order {} for user {}", orderId, userId);`
- **内容:** `ERROR` 级别日志必须包含完整的堆栈信息。

### 不变性 (Immutability)
- **DTO/VO:** 优先设计为不可变对象（使用`final`字段，不提供setter）。
- **集合:** 对外暴露的集合应使用 `Collections.unmodifiableList()` 等进行包装。

## 3. 禁止事项
- 禁止返回 `null` 集合，应返回空集合 (e.g., `Collections.emptyList()`)。
- 禁止在业务代码中使用 `System.out.println`，应统一使用日志框架。
```

---

### **前端 (Vue + JS) 编码规范 (`frontend-coding-spec.md`)**

```markdown
# 前端 (Vue + JS) 编码规范 (v1.2)

本规范旨在确保前端代码库的一致性、可维护性和性能。所有代码都应通过 `ESLint` 和 `Prettier` 的自动检查。

## 1. JavaScript / TypeScript
- **变量:** 优先使用 `const`。禁止使用 `var`。
- **模块化:** 全部使用 ES6 模块 (`import`/`export`)。
- **类型:** 推荐使用 TypeScript。所有 `props`, `store`, `API` 响应都应有明确的类型定义。

## 2. Vue 组件开发
- **语法:** 优先使用 `<script setup>` 语法。
- **命名:** 组件文件名和组件名均使用 `PascalCase` (e.g., `BaseButton.vue`)。
- **Props:**
  - 必须有明确的 `type`。
  - 非 `Boolean` 类型的非必需`prop`必须提供 `default` 值。
- **Events:** `emit` 的事件名使用 `kebab-case` (e.g., `@update:model-value`)。
- **响应式:** 优先使用 `ref` 和 `reactive`。对于大型、只读数据，使用 `shallowRef` 来优化性能。

## 3. CSS 与样式
- **作用域:** 必须使用 `<style scoped>` 来避免全局样式污染。
- **方法论:** 推荐使用 BEM (`.block__element--modifier`) 或 utility-first (如 TailwindCSS) 来组织CSS类名。
- **变量:** 颜色、字体大小、间距等应定义为CSS变量，便于维护。
  ```css
  :root {
    --primary-color: #42b983;
    --font-size-base: 16px;
  }
  ```

## 4. 可访问性 (Accessibility - A11y)
- **语义化HTML:** 使用正确的HTML标签 (e.g., `<nav>`, `<button>`, `<main>`)。
- **图像:** 所有 `<img>` 标签必须有 `alt` 属性。
- **表单:** 所有表单输入控件都应与 `<label>` 关联。
- **键盘导航:** 确保所有可交互元素都可以通过键盘（Tab键）访问和操作。

## 5. 错误处理
- **API请求:** 必须有统一的错误处理逻辑（如使用Axios拦截器），能优雅地处理网络和服务器错误。
- **组件边界:** 考虑使用Vue的 `onErrorCaptured` 钩子或错误边界组件来捕获组件内部错误，防止整个应用崩溃。