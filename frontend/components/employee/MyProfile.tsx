"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { EmployeeResponse } from "@/types/hr";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { UserCircle2, Mail, Phone, MapPin, Building, Briefcase, Edit2 } from "lucide-react";
import { useAuthStore } from "@/store/authStore";
import { EditProfileModal } from "./EditProfileModal";
import { Button } from "@/components/ui/Button";

export function MyProfile() {
  const { user } = useAuthStore();
  const [profile, setProfile] = useState<EmployeeResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        setIsLoading(true);
        const data = await hrRepository.getMyProfile();
        setProfile(data);
      } catch (err: any) {
        setError(err.message || "Failed to load profile");
      } finally {
        setIsLoading(false);
      }
    };
    loadProfile();
  }, []);

  const handleProfileUpdated = async () => {
    setIsEditModalOpen(false);
    setIsLoading(true);
    try {
      const data = await hrRepository.getMyProfile();
      setProfile(data);
    } catch (err: any) {
      setError(err.message || "Failed to reload profile");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <LoadingState message="Loading your profile..." />;
  if (error) return <ErrorState message={error} />;
  if (!profile) return <ErrorState message="Profile not found" />;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-foreground">My Profile</h2>
          <p className="text-muted-foreground mt-1">Manage your personal and professional information.</p>
        </div>
        <Button onClick={() => setIsEditModalOpen(true)} className="flex items-center gap-2">
          <Edit2 className="w-4 h-4" />
          Edit Profile
        </Button>
      </div>

      <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden">
        <div className="p-8 border-b border-border bg-surface-hover/30 flex items-center gap-6">
          <div className="w-24 h-24 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-3xl border-4 border-surface shadow-sm">
            {profile.first_name[0]}{profile.last_name[0]}
          </div>
          <div>
            <h3 className="text-2xl font-bold text-foreground">
              {profile.first_name} {profile.last_name}
            </h3>
            <div className="flex items-center gap-2 mt-2 text-muted-foreground">
              <Briefcase className="w-4 h-4" />
              <span>{profile.designation_id ? "Designation ID: " + profile.designation_id : "Employee"}</span>
            </div>
          </div>
        </div>

        <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-6">
            <h4 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-4 border-b border-border pb-2">
              Contact Information
            </h4>
            
            <div className="flex items-start gap-3">
              <Mail className="w-5 h-5 text-muted-foreground mt-0.5" />
              <div>
                <p className="text-xs font-medium text-muted-foreground">Email Address</p>
                <p className="text-sm font-medium text-foreground">{user?.email || "Not provided"}</p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <Phone className="w-5 h-5 text-muted-foreground mt-0.5" />
              <div>
                <p className="text-xs font-medium text-muted-foreground">Phone Number</p>
                <p className="text-sm font-medium text-foreground">{profile.phone || "Not provided"}</p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <MapPin className="w-5 h-5 text-muted-foreground mt-0.5" />
              <div>
                <p className="text-xs font-medium text-muted-foreground">Work Location</p>
                <p className="text-sm font-medium text-foreground">{profile.work_location || "Not provided"}</p>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <h4 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-4 border-b border-border pb-2">
              Employment Details
            </h4>
            
            <div className="grid grid-cols-2 gap-6">
              <div>
                <p className="text-xs font-medium text-muted-foreground">Employee Code</p>
                <p className="text-sm font-medium text-foreground">{profile.employee_code}</p>
              </div>
              
              <div>
                <p className="text-xs font-medium text-muted-foreground">Status</p>
                <Badge variant={profile.employment_status === "ACTIVE" ? "success" : "secondary"} className="mt-1">
                  {profile.employment_status}
                </Badge>
              </div>
              
              <div>
                <p className="text-xs font-medium text-muted-foreground">Employment Type</p>
                <p className="text-sm font-medium text-foreground capitalize">{profile.employment_type.toLowerCase()}</p>
              </div>
              
              <div>
                <p className="text-xs font-medium text-muted-foreground">Joining Date</p>
                <p className="text-sm font-medium text-foreground">
                  {new Date(profile.joining_date).toLocaleDateString()}
                </p>
              </div>
              
              <div>
                <p className="text-xs font-medium text-muted-foreground">Department</p>
                <p className="text-sm font-medium text-foreground">
                  {profile.department_id ? "Department ID: " + profile.department_id : "None"}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {isEditModalOpen && profile && (
        <EditProfileModal
          profile={profile}
          onClose={() => setIsEditModalOpen(false)}
          onSuccess={handleProfileUpdated}
        />
      )}
    </div>
  );
}
