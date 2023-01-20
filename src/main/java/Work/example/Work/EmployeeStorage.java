package Work.example.Work;

import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class EmployeeStorage {

    private Employee employee;

    private static List<Employee> employeeList = new ArrayList<>();

    public EmployeeStorage() {
        employeeList.add(new Employee(1,22,"Sprzedawca",Department.SALES));
        employeeList.add(new Employee(2,4000,"Pomoc Techniczna",Department.IT));

    }

    public List<Employee> getEmployeeList() {
        return employeeList;
    }


}
