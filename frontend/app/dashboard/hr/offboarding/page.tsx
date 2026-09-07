"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { EmployeeResponse, OffboardingTaskResponse } from "@/types/hr";
import { Button } from "@/components/ui/Button";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import toast from "react-hot-toast";

export default function OffboardingPage() {
  const [employees, setEmployees] = useState<EmployeeResponse[]>([]);
  const [selectedEmployee, setSelectedEmployee] = useState<string>("");
  const [tasks, setTasks] = useState<OffboardingTaskResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTaskName, setNewTaskName] = useState("");
  const [isAddingTask, setIsAddingTask] = useState(false);

  useEffect(() => {
    fetchEmployees();
  }, []);

  useEffect(() => {
    if (selectedEmployee) {
      fetchTasks(selectedEmployee);
    } else {
      setTasks([]);
    }
  }, [selectedEmployee]);

  const fetchEmployees = async () => {
    try {
      setIsLoading(true);
      const data = await hrRepository.getEmployees();
      // Show terminated/resigned or active employees that might be leaving
      setEmployees(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load employees");
    } finally {
      setIsLoading(false);
    }
  };

  const fetchTasks = async (employeeId: string) => {
    try {
      const data = await hrRepository.getOffboardingTasks(employeeId);
      setTasks(data);
    } catch (err: unknown) {
      toast.error("Failed to load tasks");
    }
  };

  const handleAddTask = async () => {
    if (!newTaskName.trim() || !selectedEmployee) return;
    try {
      setIsAddingTask(true);
      await hrRepository.createOffboardingTask({
        employee_id: selectedEmployee,
        task_name: newTaskName,
      });
      setNewTaskName("");
      toast.success("Task added");
      fetchTasks(selectedEmployee);
    } catch (err: unknown) {
      toast.error("Failed to add task");
    } finally {
      setIsAddingTask(false);
    }
  };

  const handleToggleTask = async (task: OffboardingTaskResponse) => {
    try {
      await hrRepository.updateOffboardingTask(task.id, { is_completed: !task.is_completed });
      fetchTasks(selectedEmployee);
    } catch (err: unknown) {
      toast.error("Failed to update task");
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (!window.confirm("Delete task?")) return;
    try {
      await hrRepository.deleteOffboardingTask(id);
      fetchTasks(selectedEmployee);
      toast.success("Task deleted");
    } catch (err: unknown) {
      toast.error("Failed to delete task");
    }
  };

  if (isLoading) return <LoadingState message="Loading..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchEmployees} />;

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">Offboarding</h1>
        <p className="text-sm text-gray-500 mt-1">Manage offboarding checklists for departing employees.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1 border-r pr-6 space-y-4">
          <h2 className="font-semibold text-lg">Select Employee</h2>
          <div className="space-y-2">
            {employees.map(emp => (
              <button
                key={emp.id}
                onClick={() => setSelectedEmployee(emp.id)}
                className={`w-full text-left px-4 py-3 rounded-lg border transition-colors ${
                  selectedEmployee === emp.id ? 'bg-primary/5 border-primary text-primary font-medium' : 'hover:bg-gray-50 border-gray-200'
                }`}
              >
                {emp.first_name} {emp.last_name}
                <div className="text-xs text-gray-500 font-normal">{emp.employee_code}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="md:col-span-2 space-y-6">
          {!selectedEmployee ? (
            <div className="flex flex-col items-center justify-center h-64 text-gray-400 bg-gray-50 rounded-xl border border-dashed">
              <p>Select an employee to view their offboarding checklist</p>
            </div>
          ) : (
            <div className="space-y-6 bg-white p-6 rounded-xl border shadow-sm">
              <h2 className="font-semibold text-xl">Offboarding Checklist</h2>
              
              <div className="space-y-3">
                {tasks.length === 0 ? (
                  <p className="text-sm text-gray-500 italic">No tasks created yet.</p>
                ) : (
                  tasks.map(task => (
                    <div key={task.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 group transition-colors">
                      <label className="flex items-center gap-3 cursor-pointer flex-1">
                        <input
                          type="checkbox"
                          checked={task.is_completed}
                          onChange={() => handleToggleTask(task)}
                          className="w-5 h-5 rounded border-gray-300 text-primary focus:ring-primary"
                        />
                        <span className={`${task.is_completed ? 'line-through text-gray-400' : 'text-gray-700'}`}>
                          {task.task_name}
                        </span>
                      </label>
                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        className="opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 text-sm px-2 py-1 transition-opacity"
                      >
                        Delete
                      </button>
                    </div>
                  ))
                )}
              </div>

              <div className="flex gap-3 pt-4 border-t">
                <input
                  type="text"
                  placeholder="New task name..."
                  value={newTaskName}
                  onChange={e => setNewTaskName(e.target.value)}
                  className="flex-1 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                  onKeyDown={e => e.key === 'Enter' && handleAddTask()}
                />
                <Button onClick={handleAddTask} disabled={!newTaskName.trim() || isAddingTask}>
                  Add Task
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
