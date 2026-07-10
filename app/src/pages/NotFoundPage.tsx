import { Link } from "react-router-dom";
import { AppFrame } from "../components/AppFrame";

export function NotFoundPage() {
  return (
    <AppFrame title="页面未找到">
      <div className="feedback error" role="alert">
        <strong>这个页面不存在</strong>
        <span>请返回服务广场继续访问。</span>
      </div>
      <Link className="return-link" to="/services">返回服务广场</Link>
    </AppFrame>
  );
}
