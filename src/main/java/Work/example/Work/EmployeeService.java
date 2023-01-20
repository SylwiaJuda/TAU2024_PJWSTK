package Work.example.Work;

import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class EmployeeService {
    private EmployeeStorage employeeStorage;

    public EmployeeService(EmployeeStorage employeeStorage) {
        this.employeeStorage = employeeStorage;
    }
//nowy pracownik
    public Employee addEmployee(int id,double salary, String position, Department department){
        Employee flagEmployee = findEmployee(id);

        if(id <= 0){
            return null;
        }

        if (department == null){
            return null;
        }
        if(flagEmployee == null){
            Employee employee = new Employee(id, salary, position, department);
            System.out.println("Worker has been added!");
            employeeStorage.getEmployeeList().add(employee);
            return employee;

        }
        return null;
    }
// zmiana stanowiska
    public Employee changeDepartment(int id, Department department){
        if(id <= 0){
            return null;
        }
        if(findEmployee(id) == null){
            System.out.println("no employee with this id");
            return null;
        }
        if(id == findEmployee(id).getId()){
            Employee employee = findEmployee(id);
            employee.setDepartment(department);
            System.out.println("Department has been changed!");
            return employee;

        }
        return null;
    }

//zmiana stanowiska
    public Employee changePosition(int id, String position){
        if(id <= 0){
            return null;
        }
        if(findEmployee(id) == null){
            System.out.println("no employee with this id");
            return null;
        }
        if(id == findEmployee(id).getId()){
            Employee employee = findEmployee(id);
            employee.setPosition(position);
            System.out.println("Position has been changed!");
            return employee;

        }
        return null;
    }

//employee po id
    public Employee findEmployee(int id){
        for (Employee employee: employeeStorage.getEmployeeList()) {
            if(employee.getId() == id){
                return employee;
            }
        }
        return null;
    }
}
