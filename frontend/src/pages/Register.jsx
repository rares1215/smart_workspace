import { useState } from "react";
import { register, verifyEmail, resendCode } from "../api/auth";
import { useNavigate } from "react-router-dom";

const RegisterPage = () => {
    const [form, setForm] = useState({
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
    });

    const [error, setError] = useState("");
    const [verificationMode, setVerificationMode] = useState(false);
    const [verificationCode, setVerificationCode] = useState("");
    const [userId, setUserId] = useState(null);
    const [resendCooldown, setResendCooldown] = useState(0);

    const navigate = useNavigate();

    // REGISTER FORM SUBMIT
    const handleRegister = async (e) => {
        e.preventDefault();
        setError("");

        // UX ONLY — backend validează oricum restul
        if (form.password !== form.confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        try {
            const res = await register(form);
            setUserId(res.data.user_id);
            setVerificationMode(true);
        } catch (err) {
            // Show backend serializer errors directly
            const backendErr =
                err.response?.data || err.response?.data?.error || "Registration failed";
            setError(JSON.stringify(backendErr));
        }
    };

    // VERIFY EMAIL SUBMIT
    const handleVerify = async (e) => {
        e.preventDefault();
        setError("");

        try {
            await verifyEmail(userId, { code: verificationCode });
            navigate("/login");
        } catch (err) {
            const backendErr =
                err.response?.data?.error || "Invalid or expired verification code.";
            setError(backendErr);
        }
    };

    // RESEND VERIFICATION CODE
    const handleResend = async () => {
        try {
            await resendCode(userId);
            setResendCooldown(60);

            const interval = setInterval(() => {
                setResendCooldown((prev) => {
                    if (prev <= 1) {
                        clearInterval(interval);
                        return 0;
                    }
                    return prev - 1;
                });
            }, 1000);
        } catch {
            setError("Could not resend verification code.");
        }
    };

    // ================================
    // REGISTER UI
    // ================================
    if (!verificationMode) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
                <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
                    <h1 className="text-2xl font-bold mb-6 text-center">
                        Create your account
                    </h1>

                    {error && (
                        <p className="bg-red-100 text-red-600 p-2 rounded mb-4 text-sm">
                            {error}
                        </p>
                    )}

                    <form onSubmit={handleRegister} className="space-y-4">
                        <input
                            className="w-full p-2 border rounded"
                            placeholder="Username"
                            onChange={(e) => setForm({ ...form, username: e.target.value })}
                            required
                        />

                        <input
                            className="w-full p-2 border rounded"
                            placeholder="Email"
                            type="email"
                            onChange={(e) => setForm({ ...form, email: e.target.value })}
                            required
                        />

                        <input
                            className="w-full p-2 border rounded"
                            placeholder="Password"
                            type="password"
                            onChange={(e) => setForm({ ...form, password: e.target.value })}
                            required
                        />

                        <input
                            className="w-full p-2 border rounded"
                            placeholder="Confirm Password"
                            type="password"
                            onChange={(e) =>
                                setForm({ ...form, confirmPassword: e.target.value })
                            }
                            required
                        />

                        <button
                            type="submit"
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded font-semibold"
                        >
                            Register
                        </button>
                    </form>
                </div>
            </div>
        );
    }

    // ================================
    // EMAIL VERIFICATION UI
    // ================================
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
            <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
                <h1 className="text-xl font-semibold mb-4 text-center">
                    Verify Your Email
                </h1>
                <p className="text-gray-600 mb-4 text-center">
                    A 6-digit code was sent to your email.
                </p>

                {error && (
                    <p className="bg-red-100 text-red-600 p-2 rounded mb-4 text-sm">
                        {error}
                    </p>
                )}

                <form onSubmit={handleVerify} className="space-y-4">
                    <input
                        className="w-full p-2 border rounded text-center tracking-widest text-2xl"
                        placeholder="------"
                        maxLength={6}
                        onChange={(e) => setVerificationCode(e.target.value)}
                    />

                    <button
                        type="submit"
                        className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded font-semibold"
                    >
                        Verify Email
                    </button>
                </form>

                <div className="text-center mt-4">
                    {resendCooldown > 0 ? (
                        <p className="text-gray-500 text-sm">
                            Resend available in {resendCooldown}s
                        </p>
                    ) : (
                        <button
                            className="text-blue-600 hover:underline text-sm"
                            onClick={handleResend}
                        >
                            Resend code
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;
