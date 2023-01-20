package Work.example.Work;

public class Employee {
    int id;
    private double salary;
    private String position;
    private  Department department;

    public Employee(int id, double salary, String position, Department department) {
        this.id = id;
        this.salary = salary;
        this.position = position;
        this.department = department;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public double getSalary() {
        return salary;
    }

    public void setSalary(double salary) {
        this.salary = salary;
    }

    public String getPosition() {
        return position;
    }

    public void setPosition(String position) {
        this.position = position;
    }

    public Department getDepartment() {
        return department;
    }

    public void setDepartment(Department department) {
        this.department = department;
    }

    @Override
    public String toString() {
        return "Employee{" +
                "id=" + id +
                ", salary=" + salary +
                ", position='" + position + '\'' +
                ", department=" + department +
                '}';
    }
}
