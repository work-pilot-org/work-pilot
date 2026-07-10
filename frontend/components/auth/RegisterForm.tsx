"use client";

import { useState } from "react";
import { User, Mail, Building, Lock, RefreshCw, Info, Loader2, Wand2, Eye, EyeOff, Copy, Check, X } from "lucide-react";
import { registerUseCase } from "@/use-cases/auth/register";
import { RegisterRequest } from "@/types/auth";
import { useRouter } from "next/navigation";

export default function RegisterForm() {
  const [formData, setFormData] = useState<RegisterRequest>({
    company_name: "",
    full_name: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const router = useRouter();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);
  const [showGeneratorPopover, setShowGeneratorPopover] = useState(false);
  const [generatedPassword, setGeneratedPassword] = useState("");

  // Password strength checks (Reusable)
  const calculateStrength = (pwd: string) => {
    const hasLength = pwd.length >= 8;
    const hasUpper = /[A-Z]/.test(pwd);
    const hasLower = /[a-z]/.test(pwd);
    const hasNumber = /[0-9]/.test(pwd);
    const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/.test(pwd);
    const score = [hasLength, hasUpper, hasLower, hasNumber, hasSpecial].filter(Boolean).length;
    return { hasLength, hasUpper, hasLower, hasNumber, hasSpecial, score };
  };
  
  const getStrengthText = (score: number, pwdLen: number) => {
    if (pwdLen === 0) return "";
    if (score <= 2) return "Weak";
    if (score <= 4) return "Medium";
    return "Strong";
  };

  const getStrengthColor = (score: number) => {
    if (score <= 2) return "bg-red-500";
    if (score <= 4) return "bg-yellow-500";
    return "bg-green-500";
  };

  const formPwdStrength = calculateStrength(formData.password);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const generateStrongPassword = () => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+";
    let password = "";
    for (let i = 0; i < 16; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    // Ensure at least one uppercase, lowercase, number, and special character
    const upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const lower = "abcdefghijklmnopqrstuvwxyz";
    const num = "0123456789";
    const special = "!@#$%^&*()_+";
    password = upper[Math.floor(Math.random() * upper.length)] +
               lower[Math.floor(Math.random() * lower.length)] +
               num[Math.floor(Math.random() * num.length)] +
               special[Math.floor(Math.random() * special.length)] +
               password.slice(4);
    
    password = password.split('').sort(() => 0.5 - Math.random()).join('');
    setGeneratedPassword(password);
  };

  const handleOpenGenerator = () => {
    generateStrongPassword();
    setShowGeneratorPopover(true);
  };

  const handleCopyGenerated = () => {
    navigator.clipboard.writeText(generatedPassword);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  const handleUsePassword = () => {
    setFormData((prev) => ({ ...prev, password: generatedPassword, confirm_password: generatedPassword }));
    setShowPassword(true);
    setShowConfirmPassword(true);
    setShowGeneratorPopover(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccessMsg(null);

    const result = await registerUseCase(formData);

    if (!result.success) {
      setError(result.error || "An error occurred");
      setIsLoading(false);
    } else {
      setSuccessMsg(result.data?.message || "Successfully registered! Redirecting to login...");
      setTimeout(() => {
        router.push("/login");
      }, 1500);
    }

    setIsLoading(false);
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      
      {/* Company Name */}
      <div className="space-y-2">
        <label className="block text-[13px] font-medium text-gray-700">Company Name</label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <Building className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="text"
            name="company_name"
            value={formData.company_name}
            onChange={handleChange}
            required
            placeholder="Workpilot Inc."
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
      </div>

      {/* Full Name */}
      <div className="space-y-2">
        <label className="block text-[13px] font-medium text-gray-700">Full Name</label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <User className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="text"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            required
            placeholder="John Doe"
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
      </div>

      {/* Work Email */}
      <div className="space-y-2">
        <label className="block text-[13px] font-medium text-gray-700">Work Email</label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <Mail className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            placeholder="name@company.com"
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
      </div>

      {/* Password and Confirm Password Row */}
      <div className="relative">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="block text-[13px] font-medium text-gray-700">Password</label>
              <button
                type="button"
                onClick={handleOpenGenerator}
                className="text-[#36307a] hover:bg-[#36307a]/10 p-1 rounded transition-colors"
                title="Password Generator"
              >
                <Wand2 className="w-4 h-4" />
              </button>
            </div>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
              <Lock className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="••••••••"
              className="block w-full pl-10 pr-10 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
            />
            <button 
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-gray-600"
            >
              {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
        </div>

        <div className="space-y-2">
          <label className="block text-[13px] font-medium text-gray-700">Confirm Password</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
              <RefreshCw className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type={showConfirmPassword ? "text" : "password"}
              name="confirm_password"
              value={formData.confirm_password}
              onChange={handleChange}
              required
              placeholder="••••••••"
              className="block w-full pl-10 pr-10 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
            />
            <button 
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-gray-600"
            >
              {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </div>

      {/* Generator Popover */}
        {showGeneratorPopover && (
          <div className="absolute z-30 top-full left-0 right-0 mt-2 md:top-[-15%] md:left-[105%] md:right-auto md:mt-0 md:w-[320px] p-4 bg-white border border-gray-200 rounded-xl shadow-xl md:shadow-2xl">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[13px] font-bold text-gray-900">Password Generator</span>
              <button type="button" onClick={() => setShowGeneratorPopover(false)} className="text-gray-400 hover:text-gray-600">
                <X className="w-4 h-4" />
              </button>
            </div>
            
            <button type="button" onClick={handleUsePassword} className="w-full bg-[#36307a] hover:bg-[#2a2468] text-white text-[13px] font-bold py-2.5 rounded-lg transition-colors mb-4">
              Use Password
            </button>

            <div className="flex items-center gap-2 mb-4">
              <div className="flex-1 bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-[14px] font-mono text-gray-800 tracking-wider break-all">
                {generatedPassword}
              </div>
              <button type="button" onClick={handleCopyGenerated} className="p-2 text-gray-500 hover:text-gray-700 bg-gray-50 border border-gray-200 rounded-lg transition-colors" title="Copy">
                {isCopied ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
              </button>
              <button type="button" onClick={generateStrongPassword} className="p-2 text-gray-500 hover:text-gray-700 bg-gray-50 border border-gray-200 rounded-lg transition-colors" title="Regenerate">
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>

            {/* Generator Strength Indicator */}
            {generatedPassword && (() => {
               const genStrength = calculateStrength(generatedPassword);
               return (
                 <div className="space-y-1.5">
                   <div className="flex gap-1 h-1">
                     {[1, 2, 3, 4, 5].map((level) => (
                       <div key={level} className={`flex-1 rounded-full transition-colors duration-300 ${level <= genStrength.score ? getStrengthColor(genStrength.score) : 'bg-gray-200'}`}></div>
                     ))}
                   </div>
                   <div className="text-[11px] text-gray-500 font-medium text-right">
                     {getStrengthText(genStrength.score, generatedPassword.length)}
                   </div>
                 </div>
               );
            })()}
          </div>
        )}
      </div>

      {/* Password Strength Indicator */}
      {formData.password.length > 0 && !showGeneratorPopover && (
        <div className="space-y-1.5 mt-1 transition-all duration-300">
          <div className="flex items-center justify-between text-[11px] font-medium">
            <span className="text-gray-500">Password strength</span>
            <span className={`${formPwdStrength.score <= 2 ? 'text-red-600' : formPwdStrength.score <= 4 ? 'text-yellow-600' : 'text-green-600'}`}>
              {getStrengthText(formPwdStrength.score, formData.password.length)}
            </span>
          </div>
          <div className="flex gap-1 h-1">
            {[1, 2, 3, 4, 5].map((level) => (
              <div 
                key={level} 
                className={`flex-1 rounded-full transition-colors duration-300 ${level <= formPwdStrength.score ? getStrengthColor(formPwdStrength.score) : 'bg-gray-200'}`}
              ></div>
            ))}
          </div>
          <div className="flex flex-wrap gap-x-3 gap-y-1 text-[10px] mt-2">
            <span className={`flex items-center gap-1 transition-colors ${formPwdStrength.hasLength ? 'text-green-600' : 'text-gray-400'}`}>
              <Check className="w-3 h-3" /> 8+ chars
            </span>
            <span className={`flex items-center gap-1 transition-colors ${formPwdStrength.hasUpper ? 'text-green-600' : 'text-gray-400'}`}>
              <Check className="w-3 h-3" /> Uppercase
            </span>
            <span className={`flex items-center gap-1 transition-colors ${formPwdStrength.hasLower ? 'text-green-600' : 'text-gray-400'}`}>
              <Check className="w-3 h-3" /> Lowercase
            </span>
            <span className={`flex items-center gap-1 transition-colors ${formPwdStrength.hasNumber ? 'text-green-600' : 'text-gray-400'}`}>
              <Check className="w-3 h-3" /> Number
            </span>
            <span className={`flex items-center gap-1 transition-colors ${formPwdStrength.hasSpecial ? 'text-green-600' : 'text-gray-400'}`}>
              <Check className="w-3 h-3" /> Special
            </span>
          </div>
        </div>
      )}

      {/* Feedback messages */}
      {error && (
        <div className="text-red-500 text-sm font-medium mt-2">
          {error}
        </div>
      )}
      
      {successMsg && (
        <div className="text-green-600 text-sm font-medium mt-2">
          {successMsg}
        </div>
      )}


      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-[#36307a] hover:bg-[#2a2468] text-white text-[14px] font-bold py-3.5 rounded-xl shadow-sm transition-all mt-4 disabled:opacity-70 flex items-center justify-center"
      >
        {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Create Account"}
      </button>

    </form>
  );
}
