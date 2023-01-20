package Work.example.Work;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.*;

public class Tests {
    private EmployeeStorage employeeStorage;
    private EmployeeService employeeService;

    @BeforeEach
    void setup(){
        this.employeeStorage = new EmployeeStorage();
        this.employeeService = new EmployeeService(employeeStorage);

    }
    @Test
    void createEmplyee(){
        var result = employeeService.addEmployee(0,22,"Sprzedawca",Department.SALES);
        assertThat(result).isEqualTo(null);

    }
    @Test
    void changeDepartment(){
        var result = employeeService.changeDepartment(5,Department.SALES);

        assertThat(result).isEqualTo(null);
    }
    @Test
    void changePosition(){
        var result = employeeService.changePosition(1,"Klasy");
        Employee flagEmplyee = new Employee(1,22,"Klasy",Department.SALES);
        assertThat(result.toString()).isEqualTo(flagEmplyee.toString());
    }
}
