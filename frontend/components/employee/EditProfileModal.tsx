"use client";

import { useState } from "react";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { X } from "lucide-react";
import { hrRepository } from "@/repositories/hrRepository";
import { EmployeeResponse } from "@/types/hr";

const editProfileSchema = z.object({
  phone: z.string().min(10, "Phone number must be at least 10 digits").max(15, "Phone number is too long").optional().or(z.literal("")),
  work_location: z.string().optional().or(z.literal("")),
  gender: z.enum(["MALE", "FEMALE", "OTHER"]).optional().or(z.literal("")),
  date_of_birth: z.string().optional().or(z.literal("")),
});

type EditProfileFormData = z.infer<typeof editProfileSchema>;

interface EditProfileModalProps {
  profile: EmployeeResponse;
  onClose: () => void;
  onSuccess: () => void;
}

export function EditProfileModal({ profile, onClose, onSuccess }: EditProfileModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<EditProfileFormData>({
    resolver: zodResolver(editProfileSchema),
    defaultValues: {
      phone: profile.phone || "",
      work_location: profile.work_location || "",
      gender: profile.gender || "",
      date_of_birth: profile.date_of_birth ? new Date(profile.date_of_birth).toISOString().split('T')[0] : "",
    },
  });

  const onSubmit = async (data: EditProfileFormData) => {
    try {
      setIsSubmitting(true);
      setError(null);
      // Clean up empty strings to undefined to match backend expectations
      const payload = {
        phone: data.phone || undefined,
        work_location: data.work_location || undefined,
        gender: data.gender || undefined,
        date_of_birth: data.date_of_birth || undefined,
      };
      await hrRepository.updateMyProfile(payload);
      onSuccess();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || "Failed to update profile");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-surface border border-border shadow-lg rounded-xl w-full max-w-md overflow-hidden flex flex-col max-h-[90vh]">
        <div className="p-4 border-b border-border flex items-center justify-between bg-surface-hover/30">
          <h2 className="text-lg font-semibold text-foreground">Edit Profile</h2>
          <Button variant="ghost" size="sm" onClick={onClose} className="h-8 w-8 p-0 rounded-full">
            <X className="h-4 w-4" />
          </Button>
        </div>

        <div className="p-6 overflow-y-auto">
          {error && (
            <div className="mb-4 p-3 bg-error/10 border border-error/20 text-error rounded-lg text-sm">
              {error}
            </div>
          )}

          <form id="edit-profile-form" onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Phone Number</label>
              <Input
                {...register("phone")}
                placeholder="+1234567890"
              />
              {errors.phone && <p className="text-xs text-error mt-1">{errors.phone.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Work Location</label>
              <Input
                {...register("work_location")}
                placeholder="e.g. New York, Remote"
              />
              {errors.work_location && <p className="text-xs text-error mt-1">{errors.work_location.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Gender</label>
              <select
                {...register("gender")}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <option value="">Select Gender</option>
                <option value="MALE">Male</option>
                <option value="FEMALE">Female</option>
                <option value="OTHER">Other</option>
              </select>
              {errors.gender && <p className="text-xs text-error mt-1">{errors.gender.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Date of Birth</label>
              <Input
                type="date"
                {...register("date_of_birth")}
              />
              {errors.date_of_birth && <p className="text-xs text-error mt-1">{errors.date_of_birth.message}</p>}
            </div>
          </form>
        </div>

        <div className="p-4 border-t border-border bg-surface-hover/30 flex justify-end gap-3">
          <Button variant="outline" onClick={onClose} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button type="submit" form="edit-profile-form" disabled={isSubmitting}>
            {isSubmitting ? "Saving..." : "Save Changes"}
          </Button>
        </div>
      </div>
    </div>
  );
}
