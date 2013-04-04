#ifndef __PROBES_H
#define __PROBES_H

#include "Probe.h"

namespace dolfin
{
  class Probes 
  {
      
  public:
      
    Probes(const Array<double>& x, const FunctionSpace& V);

    Probes() {};
    
    virtual ~Probes();
    
    // evaluate all probes
    virtual void eval(const Function& u);
    
    // dump component i of probes to filename
    void dump(std::size_t i, std::string filename);
    
    // dump all probes to filename
    void dump(std::string filename);
    
    // Return an instance of probe i
    virtual Probe* get_probe(std::size_t i);
    
    // Return id of probe i
    std::size_t get_probe_id(std::size_t i);
    
    // Return the number of probes on this process
    std::size_t local_size() {return _allprobes.size();};
    
    // Return number of components probed for
    std::size_t value_size() {return _value_size;};
        
    // Return total number of probes on all processes combined
    std::size_t get_total_number_probes() {return total_number_probes;};
    
    // Return number of evaluations of probes
    std::size_t number_of_evaluations() {return _num_evals;};
    
    // Erase one snapshot ot the all probes
    virtual void erase_snapshot(std::size_t i);
    
    // Reset probe by deleting all previous evaluations
    void clear();

  protected:
      
    std::vector<std::pair<std::size_t, Probe*> > _allprobes;
    
    std::size_t total_number_probes, _value_size, _num_evals;

  };  
}

#endif
