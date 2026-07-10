import { useState } from "react";
import { useAuth } from "../auth/AuthContext";

const phonePattern = /^1[3-9]\d{9}$/;

export function AuthPanel() {
  const { sendCode, login } = useAuth();
  const [phone, setPhone] = useState("");
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState<"send" | "login" | null>(null);

  const requestCode = async () => {
    if (!phonePattern.test(phone)) {
      setError("请输入正确的手机号");
      return;
    }
    setBusy("send");
    setError("");
    setMessage("");
    try {
      await sendCode(phone);
      setMessage("验证码已发送，请通过配置的测试渠道获取。页面不会显示验证码。");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "验证码发送失败");
    } finally {
      setBusy(null);
    }
  };

  const submitLogin = async () => {
    if (!phonePattern.test(phone) || !code.trim()) {
      setError("请输入手机号和验证码");
      return;
    }
    setBusy("login");
    setError("");
    setMessage("");
    try {
      await login(phone, code.trim());
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "登录失败");
    } finally {
      setBusy(null);
    }
  };

  return (
    <section className="auth-panel" aria-labelledby="auth-title">
      <h2 id="auth-title">登录后使用核心服务</h2>
      <p>登录状态仅保存在当前浏览器会话中，不会写入项目文件。</p>
      <label>
        手机号
        <input
          inputMode="tel"
          maxLength={11}
          value={phone}
          onChange={(event) => setPhone(event.target.value.replace(/\D/g, ""))}
          placeholder="请输入手机号"
        />
      </label>
      <div className="code-row">
        <label>
          验证码
          <input
            inputMode="numeric"
            maxLength={6}
            value={code}
            onChange={(event) => setCode(event.target.value.replace(/\D/g, ""))}
            placeholder="6 位验证码"
          />
        </label>
        <button type="button" onClick={requestCode} disabled={Boolean(busy)}>
          {busy === "send" ? "发送中…" : "发送验证码"}
        </button>
      </div>
      {message && <div className="auth-message" role="status">{message}</div>}
      {error && <div className="auth-error" role="alert">{error}</div>}
      <button className="primary-action" type="button" onClick={submitLogin} disabled={Boolean(busy)}>
        {busy === "login" ? "登录中…" : "登录"}
      </button>
    </section>
  );
}
